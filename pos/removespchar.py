import re
import sys
fileName = open("porterWords.txt",'r')
stop=open("removedspchar.txt",'w')
stop.write("")
while 1:
	line=fileName.readline()
	if line=='':
		break
	if re.match("^[a-zA-Z0-9]*$",line):
		stop.write(line)
		


