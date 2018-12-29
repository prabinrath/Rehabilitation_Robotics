import time
from roboclaw import Roboclaw

rc = Roboclaw("COM10",115200)
rc.Open()
address = 0x80
dis=0
spd=2700

def mapData(pos):
	return int((float(pos)/360)*2000)

'''
rc.SpeedAccelDeccelPositionM1(address,0,0,0,0,0)
time.sleep(10)
cur=rc.ReadEncM1(address)[1]
while(True):
	print spd,' ',cur-rc.ReadEncM1(address)[1]
	cur=rc.ReadEncM1(address)[1]
	rc.SpeedDistanceM1(address,spd,1,0) #speed argument is top speed(sign specifies direction),distance is always positive,distance has to be tuned for achiving desired results
	#rc.SpeedAccelDeccelPositionM1(address,0,0,0,pos,0) #speed accel deccel are max values,with all zeros it acts as servo with all max (-1000 to 1000) maps to (-180 to 180), thus motor resolution in degrees is 360/2000=0.18 degrees
	time.sleep(10)
print pos," ",rc.ReadEncM1(address)[1]
'''
'''
cur=0
while cur<1000:
	rc.SpeedAccelDeccelPositionM1(address,0,0,0,-1000,0)
	time.sleep(2)
	rc.SpeedDistanceM1(address,spd,dis,0)
	time.sleep(2)
	cur=rc.ReadEncM1(address)[1]
	print cur,' ',dis
	dis+=10
'''
'''
while(True):
	rc.SpeedAccelDeccelPositionM1(address,0,0,0,1000,0)
	time.sleep(2)
	print rc.ReadEncM1(address)[1]
	rc.SpeedAccelDeccelPositionM1(address,0,0,0,-1000,0)
	time.sleep(2)
	print rc.ReadEncM1(address)[1]
'''
'''
rc.SpeedAccelDeccelPositionM1(address,0,0,0,0,0)
time.sleep(1)

while True:
	rc.SetEncM1(address,0)
	rc.SpeedAccelDeccelPositionM1(address,0,0,0,-1000,0)
	Kdata=rc.ReadM1PositionPID(address)
	print Kdata
	time.sleep(2)
	print rc.ReadEncM1(address)[1]
'''	
rc.SetEncM1(address,0)
en=rc.ReadEncM1(address)[1]
print en
rc.SpeedAccelDeccelPositionM1(address,-300,150,0,mapData(180),0)
time.sleep(7)
en+=rc.ReadEncM1(address)[1]
rc.SetEncM1(address,0)
rc.SpeedAccelDeccelPositionM1(address,-300,300,0,mapData(29.7202),0)
time.sleep(2)
en+=rc.ReadEncM1(address)[1]
print en