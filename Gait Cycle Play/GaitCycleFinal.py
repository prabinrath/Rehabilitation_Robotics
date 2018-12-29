import time
import random
from roboclaw import Roboclaw

rc1 = Roboclaw("COM10",115200)
rc1.Open()
rc2 = Roboclaw("COM12",115200)
rc2.Open()
address = 0x80
dat=open("data_final_leftleg_mod.txt", "r+")
Kph = 700;Kih =0.001;Kdh = 120
Kpk = 900;Kik =0.001;Kdk = 120
time_step=0.015

hipList=[]
kneeList=[]

def mapSpeed(spd):
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

rc1.SetEncM1(address,0)
rc2.SetEncM1(address,0)
	
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
print len(hipList),' ',len(kneeList)