import time
import random
from roboclaw import Roboclaw
import socket

HOST = '0.0.0.0'  
PORT = 44444    
BUFFER_SIZE = 1024    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

rc1 = Roboclaw("COM10",115200)
rc1.Open()
rc2 = Roboclaw("COM12",115200)
rc2.Open()
address = 0x80
Kph = 400;Kih =0.0001;Kdh = 100
Kpk = 600;Kik =0.001;Kdk = 10
rc1.SetEncM1(address,0)
rc2.SetEncM1(address,0)

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
	
def takeActionCombined(setPointH,setPointK):
	flagH=False;flagK=False
	p_e_h = 0;i_e_h = 0;d_e_h = 0;e_curr_h = 0;e_prev_h = 0;
	p_e_k = 0;i_e_k = 0;d_e_k = 0;e_curr_k = 0;e_prev_k = 0;
	while True:
		cur=rc1.ReadEncM1(address)[1]
		if cur>setPointH-7 and cur<setPointH+7:
			if flagH==False:
				print 'Reached Hip point:',cur,' Target was: ',setPointH
				rc1.DutyM1(address,0)
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
		if cur>setPointK-7 and cur<setPointK+7:
			if flagK==False:
				print 'Reached Knee point:',cur,' Target was: ',setPointK
				rc2.DutyM1(address,0)
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

init=time.clock()
while True:
	try:
	    data = s.recvfrom(BUFFER_SIZE)
	    if data:
	        val=getDataArray(data[0])
	        if time.clock()-init>0.0005:
	        	takeActionCombined(mapData(val[0]),mapData(val[1]))
	        	print val
	        	init=time.clock()
	except KeyboardInterrupt:
		s.close()
		rc1.DutyM1(address,0)
		rc2.DutyM1(address,0)
