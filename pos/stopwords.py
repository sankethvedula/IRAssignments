from nltk.corpus import stopwords
stop=stopwords.words('english')
fileName=open("removedspchar.txt",'r')
stopped=open("afterStop.txt",'w')
stopped.write("")
while 1:
	line=fileName.readline()
	
	if line=='':
		break
	length=len(line)-1
	line=line[0:length]
	if line not in stop:
		stopped.write(line)
		stopped.write("\n")
	
