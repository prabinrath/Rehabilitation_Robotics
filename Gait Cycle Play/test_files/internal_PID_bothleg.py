import time
import random
from roboclaw import Roboclaw

rc = Roboclaw("/dev/ttyACM0",115200)
rc.Open()
address = 0x80
dat=open("data_final_leftleg.txt", "r+")

cur_posHip=0;cur_posKnee=0

def takeAction(posHip,posKnee):
	global cur_posHip,cur_posKnee
	
	posHip=-int((float(posHip)/360)*2000)
	posKnee=-int((float(posKnee)/360)*2000)
	
	dposHip=posHip-cur_posHip
	dposKnee=posKnee-cur_posKnee
	
	rc.SetEncM1(address,0)
	rc.SetEncM2(address,0)
	
	if dposHip<0:
		rc.SpeedAccelDeccelPositionM1(address,0,0,0,dposHip-20,0)
	elif dposHip>0:
		rc.SpeedAccelDeccelPositionM1(address,0,0,0,dposHip+20,0)
	else:
		rc.SpeedAccelDeccelPositionM1(address,0,0,0,0,0)
		
	if dposKnee<0:
		rc.SpeedAccelDeccelPositionM2(address,0,0,0,dposKnee-20,0)
	elif dposKnee>0:
		rc.SpeedAccelDeccelPositionM2(address,0,0,0,dposKnee+20,0)
	else:
		rc.SpeedAccelDeccelPositionM1(address,0,0,0,0,0)

	while abs(rc.ReadEncM2(address)[1])<abs(dposKnee):
		print 'M2'
	while abs(rc.ReadEncM1(address)[1])<abs(dposHip):
		print 'M1'
		
	print cur_posHip,' ',dposHip,' ',cur_posKnee,' ',dposKnee
	cur_posHip=posHip
	cur_posKnee=posKnee

while True:
	line = dat.readline()
	if line=='':
		break
	val=line.split(',')
	takeAction(val[0],val[1])
