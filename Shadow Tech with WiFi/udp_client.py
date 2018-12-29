'''
UDP connection test
Author: Prabin Rath
'''
import socket
HOST = '192.168.43.22'  
PORT = 44444    
BUFFER_SIZE = 1024    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

def getDataArray(encoded):
	encoded=encoded.decode() #for Python 3.6
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

while True:
    data = s.recvfrom(BUFFER_SIZE)
    if data:
        try:
            val=getDataArray(data[0])
            '''
            val[1]-=val[0]
            if val[0]<-35:
                val[0]=-35
            elif val[0]>0:
                val[0]=0
            if val[1]>54:
                val[1]=54
            elif val[1]<0:
                val[1]=0
            print str(-val[0]+90)+"  "+str(-val[1]+89.99)
            '''
            print str(val[0])+" "+str(val[1])
        except:
            print val
s.close()
