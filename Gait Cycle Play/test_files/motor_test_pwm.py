import time
from roboclaw import Roboclaw

#rc1 = Roboclaw("COM10",115200)
#rc1.Open()
rc2 = Roboclaw("COM12",115200)
rc2.Open()

address = 0x80

speed=100

while(1):
	'''
	pos=rc1.ReadEncM1(address)[1]
	spd=rc1.ReadSpeedM1(address)[1]
	print 'Given speed: ',speed,' Encoder Position: ',pos,' Encoder Speed: ',spd
	'''
	#rc.SpeedM1(address,speed) #provides lower resolution,dosent require encoders for functioning,speed arguments are in range of the encoder outputs
	#rc1.DutyM1(address,speed) #provides higher resolution,dosent require encoders for functioning,data argument range is -32768 to +32767
	rc2.DutyM1(address,speed)
	time.sleep(0.1)
	speed+=100
	print speed

rc1.SpeedM1(address,0)
#rc2.SpeedM1(address,0)
