import time
import random
from roboclaw import Roboclaw

rc = Roboclaw("COM7",115200)
rc.Open()
address = 0x80
dat=open("data_final_leftleg_mod.txt", "r+")
Kp = 600;Ki =0.001;Kd = 120
time_step=0.015
rc.SetEncM1(address,0)
time.sleep(1)

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

def takeAction(setPoint):
	p_e=0;i_e=0;d_e=0;e_prev = 0;e_curr = 0;
	while True:
		cur=rc.ReadEncM1(address)[1]
		if cur>setPoint-2 and cur<setPoint+2:
			print 'Reached'
			rc.DutyM1(address,0)
			return
		e_curr = setPoint - cur
		i_e = p_e + e_curr
		if i_e>100 or i_e<-100:
				i_e=0
		p_e = e_curr
		d_e = e_curr - e_prev
		u = Kp * p_e + Ki * i_e + Kd * d_e
		e_prev=e_curr
		print p_e,' ',d_e,' ',i_e,' ',u,' ',mapSpeed(u)
		rc.DutyM1(address,mapSpeed(u))

#takeAction(mapData(209.54)) #too fast
#time.sleep(2)
'''
#get to the initial position
rc.SetEncM1(address,0)
en=rc.ReadEncM1(address)[1]
print en
rc.SpeedAccelDeccelPositionM1(address,300,150,0,mapData(180),0)
time.sleep(7)
en+=rc.ReadEncM1(address)[1]
rc.SetEncM1(address,0)
rc.SpeedAccelDeccelPositionM1(address,300,300,0,mapData(29.7202),0)
time.sleep(2)
en+=rc.ReadEncM1(address)[1]
print en
time.sleep(5)
rc.SetEncM1(address,0)
'''
while True:
	line = dat.readline()
	if line=='':
		break
	val=line.split(',')
	init_time=time.clock()
	takeAction(mapData(val[1]))
	while time.clock()-init_time<=time_step:
		{
		}
rc.SpeedM1(address,0)
