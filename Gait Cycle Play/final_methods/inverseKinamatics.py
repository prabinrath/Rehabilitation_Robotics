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

#right knee joint
def getRightKnee(alpharsipr):
	#alpharsipr=89
	VHRShsipr = 20*math.sin(math.pi/2 - alpharsipr*math.pi/180)
	VHRSvsipr = 20- 20*math.cos(math.pi/2-alpharsipr*math.pi/180)
	VHRShysipr = math.sqrt(VHRShsipr**2 + VHRSvsipr**2)
	angleVHcossipr = math.acos(VHRShsipr/VHRShysipr)
	angleVHsinsipr = math.asin(VHRShsipr/VHRShysipr)
	anglesVHhysipr = math.pi-angleVHcossipr
	sshsipr = math.sqrt(pressh**2+VHRShysipr**2-2*VHRShysipr*pressh*math.cos(anglesVHhysipr))
	alphacrsiprex=math.acos((sshsipr**2+pressh**2-VHRShysipr**2)/(2*sshsipr*pressh))
	Drsipr=math.sqrt(sshsipr**2+lsh**2-2*sshsipr*lsh*math.cos(alphacrsiprex+alpharsipr*math.pi/180))
	alphacrsipr=(math.acos((Drsipr**2+psh**2-qsh**2)/(2*Drsipr*psh))+math.acos((Drsipr**2+sshsipr**2-lsh**2)/(2*Drsipr*sshsipr)))*180/math.pi
	thetarersipr=3*(alphacrsipr+alphacrsiprex*180/math.pi)
	#print(thetarersipr)
	return thetarersipr

#right hip
def getRightHip(alphartipr):
	#alphartipr=115
	Drtipr=math.sqrt(sth**2+lth**2-2*sth*lth*math.cos(alphartipr*math.pi/180))
	alphacrtipr=(math.acos((Drtipr**2+pth**2-qth**2)/(2*Drtipr*pth))+math.acos((Drtipr**2+sth**2-lth**2)/(2*Drtipr*sth)))*180/math.pi
	thetarertipr=3*alphacrtipr
	#print(thetarertipr)
	return thetarertipr

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

print getRightKnee(70.91)