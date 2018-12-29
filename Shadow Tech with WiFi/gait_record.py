'''
Gait cycle record
Author: Prabin Rath
'''
import socket
from threading import Thread

#Setup network setup
HOST = '0.0.0.0'  
PORT = 44444    
BUFFER_SIZE = 1024    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
dat=open("debasis.txt", "w")
flag=False

#Thread function for recording the gait cycle
def recordControl():
    global flag
    print 'Thread started'
    while True:
        inp=raw_input()
        print inp
        if inp=='t':
            flag=True
        else:
            flag=False

#decoding function
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

t=Thread(target=recordControl)
t.start()

#to terminate the loop press CTRL+C
while True:
    data = s.recvfrom(BUFFER_SIZE)
    if data:
        try:
            val=getDataArray(data[0])
            print str(val[0])+" "+str(val[1])+" "+str(flag)
            if flag==True:
                dat.write(str(val[0])+","+str(val[1])+",\n")
        except:
            print val
s.close()
