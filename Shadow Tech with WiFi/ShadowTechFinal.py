import time
import random
from roboclaw import Roboclaw
import socket
import math

pressh =52.85379
psh = 26.26848
qsh = 154.1493
lsh = 170.8741
ssh = math.sqrt(pressh**2 + 400)
sth = 99.63802
pth = 39.23936
qth = 195.3119
lth = 138.6887

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

#left hip
def getLeftHip(alphaltipr):
	#alphaltipr=90
	Dltipr=math.sqrt( sth**2 + lth**2 - 2 * sth * lth * math.cos(alphaltipr*math.pi/180))
	alphacltipr=(math.acos((Dltipr**2+pth**2-qth**2)/(2*Dltipr*pth))+math.acos((Dltipr**2+sth**2-lth**2)/(2*Dltipr*sth)))*180/math.pi
	thetareltipr=3*alphacltipr
	#print(thetareltipr)
	return thetareltipr

#left knee
def getLeftKnee(alphalsipr):
	#alphalsipr=69
	VHLShsipr=20*math.sin(math.pi/2-alphalsipr*math.pi/180)
	VHLSvsipr=20-20*math.cos(math.pi/2-alphalsipr*math.pi/180)
	VHLShysipr=math.sqrt(VHLShsipr**2+VHLSvsipr**2)
	angleVHcossipr=math.acos(VHLShsipr/VHLShysipr)
	angleVHsinsipr=math.asin(VHLShsipr/VHLShysipr)
	anglesVHhysipr=math.pi-angleVHcossipr
	lssshsipr=math.sqrt(pressh**2+VHLShysipr**2-2*VHLShysipr*pressh*math.cos(anglesVHhysipr))
	alphaclsiprex=math.acos((lssshsipr**2+pressh**2-VHLShysipr**2)/(2*lssshsipr*pressh))
	Dlsipr=math.sqrt(lssshsipr**2+lsh**2-2*lssshsipr*lsh*math.cos(alphaclsiprex+alphalsipr*math.pi/180))
	alphaclsipr=(math.acos((Dlsipr**2+psh**2-qsh**2)/(2*Dlsipr*psh))+math.acos((Dlsipr**2+lssshsipr**2-lsh**2)/(2*Dlsipr*lssshsipr)))*180/math.pi
	thetarelsipr=3*(alphaclsipr+alphaclsiprex*180/math.pi)
	#print(thetarelsipr)
	return thetarelsipr

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
	if spd<-20000:
		spd=-20000
	elif spd>20000:
		spd=20000
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
		if cur>setPointH-30 and cur<setPointH+30:
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
		if cur>setPointK-30 and cur<setPointK+30:
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

rc1.SetEncM1(address,mapData(getLeftHip(90)))
rc2.SetEncM1(address,mapData(getLeftKnee(89.99)))

init=time.clock()
while True:
	try:
	    data = s.recvfrom(BUFFER_SIZE)
	    if data:
	        val=getDataArray(data[0])
	        if time.clock()-init>0.001:
	        	try:
	        		val[1]-=val[0]
	        		if val[0]<-35:
	        			val[0]=-35
	        		elif val[0]>0:
	        			val[0]=0
	        		if val[1]>54:
	        			val[1]=54
	        		elif val[1]<0:
	        			val[1]=0
	        		#print str(-val[0]+90)+"  "+str(-val[1]+89.99)
	        		takeActionCombined(mapData(getLeftHip(-val[0]+90)),mapData(getLeftKnee(-val[1]+89.99)))
	        		init=time.clock()
	        	except:
	        		print 'Invalid Angle'
	except KeyboardInterrupt:
		s.close()
		rc1.DutyM1(address,0)
		rc2.DutyM1(address,0)