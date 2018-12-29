import time
import random
from roboclaw import Roboclaw

rc = Roboclaw("/dev/ttyACM0",115200)
rc.Open()
address = 0x80
dat=open("data_final_leftleg.txt", "r+")

cur_pos=0;

def takeAction(pos):
	global cur_pos
	pos=-int((float(pos)/360)*2000)
	dpos=pos-cur_pos
	
	rc.SetEncM1(address,0)
	if dpos<0:
		rc.SpeedAccelDeccelPositionM1(address,0,0,0,dpos-20,0)
	elif dpos>0:
		rc.SpeedAccelDeccelPositionM1(address,0,0,0,dpos+20,0)
	else:
		rc.SpeedAccelDeccelPositionM1(address,0,0,0,0,0)
		
	while abs(rc.ReadEncM1(address)[1])<abs(dpos):
		{
		}
	print cur_pos,' ',dpos
	cur_pos=pos

while True:
	line = dat.readline()
	if line=='':
		break
	val=line.split(',')
	takeAction(val[0])
