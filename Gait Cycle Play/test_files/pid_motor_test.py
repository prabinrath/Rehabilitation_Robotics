import time
import random
from roboclaw import Roboclaw

rc = Roboclaw("/dev/ttyACM0",115200)
rc.Open()
address = 0x80
Kp = 10;Ki = 0.01;Kd = 0.5;
while True:
	setPoint=random.randint(-10000,10000)
	p_e=0;i_e=0;d_e=0;e_prev = 0;e_curr = 0;
	while True:
		cur=rc.ReadEncM1(address)[1]
		spd=rc.ReadSpeedM1(address)[1]
		e_curr = setPoint - cur
		i_e = p_e + e_curr
		p_e = e_curr
		d_e = e_curr - e_prev
		u = Kp * p_e + Ki * i_e + Kd * d_e
		e_prev=e_curr
		print 'Current: ',cur,'To Reach: ',setPoint,'Speed: ',spd,' PID speed: ',u
		rc.SpeedM1(address,int(u))
		cur=rc.ReadEncM1(address)[1]
		if cur>=setPoint-2 and cur<=setPoint+2:
			break
		time.sleep(0.01)
	print 'Reached Target : ','Current ',cur,'Target ',setPoint
	time.sleep(5)
