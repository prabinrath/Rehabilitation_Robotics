import time
import random
from roboclaw import Roboclaw

rc = Roboclaw("COM7",115200)
rc.Open()
address = 0x80
dat=open("data_final_leftleg.txt", "r+")
Kph = 1000;Kpk = 700;Ki =0.01;Kd = 10
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
rc.SetEncM2(address,0)
en=rc.ReadEncM2(address)[1]
print en
rc.SpeedAccelDeccelPositionM2(address,300,150,0,mapData(180),0)
time.sleep(7)
en+=rc.ReadEncM2(address)[1]
rc.SetEncM2(address,0)
rc.SpeedAccelDeccelPositionM2(address,300,300,0,mapData(29.7202),0)
time.sleep(2)
en+=rc.ReadEncM2(address)[1]
print en
time.sleep(5)

rc.SetEncM1(address,0)
rc.SetEncM2(address,0)
	
def takeActionCombined(setPointH,setPointK):
	p_e = 0;i_e = 0;d_e = 0;e_curr = 0;e_prev = 0;
	while True:
		cur=rc.ReadEncM1(address)[1]
		if cur>setPointH-3 and cur<setPointH+3:
			print 'Reached Hip point:',cur,' Target was: ',setPointH
			rc.DutyM1(address,0)
			hipList.append(-((cur/2000)*360))
			break
		else:
			e_curr = setPointH - cur
			i_e = p_e + e_curr
			if i_e>100 or i_e<-100:
				i_e=0
			p_e = e_curr
			d_e = e_curr - e_prev
			u = Kph * p_e + Ki * i_e + Kd * d_e
			e_prev_h=e_curr
			rc.DutyM1(address,mapSpeed(u))
		print 'PID Running'
	p_e = 0;i_e = 0;d_e = 0;e_curr = 0;e_prev = 0;
	while True:	
		cur=rc.ReadEncM2(address)[1]
		if cur>setPointK-3 and cur<setPointK+3:
			print 'Reached Knee point:',cur,' Target was: ',setPointK
			rc.DutyM2(address,0)
			kneeList.append(-((cur/2000)*360))
			break
		else:
			e_curr = setPointK - cur
			i_e = p_e + e_curr
			if i_e>100 or i_e<-100:
				i_e=0
			p_e = e_curr
			d_e = e_curr - e_prev
			u = Kpk * p_e + Ki * i_e + Kd * d_e
			e_prev_k=e_curr
			rc.DutyM2(address,mapSpeed(u))
		print 'PID Running'

while True:
	line = dat.readline()
	if line=='':
		break
	val=line.split(',')
	#print val
	init_time=time.clock()
	takeActionCombined(mapData(val[0]),mapData(val[1]))
	while time.clock()-init_time<=time_step:
		{
		}
rc.DutyM1(address,0)
rc.DutyM2(address,0)
print len(hipList),' ',len(kneeList)
