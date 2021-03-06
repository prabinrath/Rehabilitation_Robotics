'''
PID Controller for gait cycle play
Author: Prabin Rath
'''
import time
import random
from roboclaw import Roboclaw

#Change the COM ports with change in system
#Kp is most effective tem to handle
rc1 = Roboclaw("COM10",115200)
rc1.Open()
rc2 = Roboclaw("COM12",115200)
rc2.Open()
address = 0x80
dat=open("data_final_leftleg_mod.txt", "r+")
Kph = 700;Kih =0.001;Kdh = 120
Kpk = 900;Kik =0.001;Kdk = 120
time_step=0.015

#list of reached points for feedback
hipList=[]
kneeList=[]

def mapSpeed(spd):
	'''
	Don't change the parameters here. They are with reference from User manual and experiments.
	'''
	if spd<-30768:
		spd=-30768
	elif spd>30767:
		spd=30767
	if spd<0:
		spd-=2000
	else:
		spd+=2000
	return int(spd)

def mapData(pos):
	'''
	Don't change the parameters here. They are with reference from User manual and experiments.
	'''
	return -int((float(pos)/360)*2000)

#get to the initial position
rc2.SetEncM1(address,0)
en=rc2.ReadEncM1(address)[1]
print en
rc2.SpeedAccelDeccelPositionM1(address,300,150,0,mapData(180),0)
time.sleep(7)
en+=rc2.ReadEncM1(address)[1]
rc2.SetEncM1(address,0)
rc2.SpeedAccelDeccelPositionM1(address,300,300,0,mapData(29.7202),0)
time.sleep(2)
en+=rc2.ReadEncM1(address)[1]
print en
time.sleep(5)

#set the encoders to zero initially( prevents hard moves due to mechanical errors )
rc1.SetEncM1(address,0)
rc2.SetEncM1(address,0)

#PID controller acts on two motors simultaniously
def takeActionCombined(setPointH,setPointK):
	flagH=False;flagK=False
	p_e_h = 0;i_e_h = 0;d_e_h = 0;e_curr_h = 0;e_prev_h = 0;
	p_e_k = 0;i_e_k = 0;d_e_k = 0;e_curr_k = 0;e_prev_k = 0;
	while True:
		cur=rc1.ReadEncM1(address)[1]
		if cur>setPointH-3 and cur<setPointH+3:
			if flagH==False:
				print 'Reached Hip point:',cur,' Target was: ',setPointH
				rc1.DutyM1(address,0)
				hipList.append(-((cur/2000)*360))
				flagH=True
		else:
			e_curr_h = setPointH - cur
			i_e_h = p_e_h + e_curr_h
			if i_e_h>100 or i_e_h<-100:
				i_e_h=0
			p_e_h = e_curr_h
			d_e_h = e_curr_h - e_prev_h
			u = Kph * p_e_h + Kih * i_e_h + Kdh * d_e_h
			e_prev_h=e_curr_h
			rc1.DutyM1(address,mapSpeed(u))
		
		cur=rc2.ReadEncM1(address)[1]
		if cur>setPointK-3 and cur<setPointK+3:
			if flagK==False:
				print 'Reached Knee point:',cur,' Target was: ',setPointK
				rc2.DutyM1(address,0)
				kneeList.append(-((cur/2000)*360))
				flagK=True
		else:
			e_curr_k = setPointK - cur
			i_e_k = p_e_k + e_curr_k
			if i_e_k>100 or i_e_k<-100:
				i_e_k=0
			p_e_k = e_curr_k
			d_e_k = e_curr_k - e_prev_k
			u = Kpk * p_e_k + Kik * i_e_k + Kdk * d_e_k
			e_prev_k=e_curr_k
			rc2.DutyM1(address,mapSpeed(u))
		print 'PID Running'
		if flagH==True and flagK==True:
			break

while True:
	line = dat.readline()
	if line=='':
		break
	val=line.split(',')
	#print val
	init_time=time.clock()
	takeActionCombined(-mapData(val[0]),mapData(val[1]))
	while time.clock()-init_time<=time_step:
		{
		}
rc1.DutyM1(address,0)
rc2.DutyM1(address,0)
dat.close()

#the text file will be found in the current file directory with the reached points in degrees
dat=open("record.txt", "w")
for i in range(len(hipList)):
	dat.write(str(hipList[i])+','+str(kneeList[i])+',\n')
dat.close()
