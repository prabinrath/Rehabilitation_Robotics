import time
import random
from roboclaw import Roboclaw
import socket

HOST = '0.0.0.0'  
PORT = 44444    
BUFFER_SIZE = 1024    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

rc = Roboclaw("COM12",115200)
rc.Open()
address = 0x80
Kp = 600;Ki =0.001;Kd = 200
rc.SetEncM1(address,0)

def getDataArray(encoded):
	#encoded=encoded.decode() #for Python 3.6
	dat=encoded.split('#')
	#print(dat)
	vals=[]
	for temp in dat:
		if len(temp)>0:
			try:
				vals.append(float(temp))
			except:
				pass
	return vals

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
	print setPoint
	p_e=0;i_e=0;d_e=0;e_prev = 0;e_curr = 0;
	while True:
		cur=rc.ReadEncM1(address)[1]
		if cur>setPoint-7 and cur<setPoint+7:
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
		rc.DutyM1(address,mapSpeed(u))

init=time.clock()
while True:
	try:
	    data = s.recvfrom(BUFFER_SIZE)
	    if data:
	        val=getDataArray(data[0])
	        if time.clock()-init>0.001:
	        	takeAction(mapData(val[0]))
	        	print val
	        	init=time.clock()
	except KeyboardInterrupt:
		s.close()
		rc.DutyM1(address,0)