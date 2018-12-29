dat=open("mod_data_0.18.txt", "r+")
wrt=open("data_final_leftleg_mod.txt", "w+")

while True:
	line = dat.readline()
	if line=='':
		break
	val=line.split(',')
	s=''
	s+=val[0].split('\t')[0]
	s+=','
	s+=val[1].split('\t')[1].split('\r')[0]
	s+=',\n'
	wrt.write(s)
