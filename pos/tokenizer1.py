import nltk
import sys
from nltk.corpus import stopwords
import re

i = 0
file_tokenied="tokenized1.txt"
file_porter="porterWords1.txt"
file_boolean = "filePlusDocID.txt"
stop=stopwords.words('english')
f1=open(file_tokenied,"w")
fp=open(file_porter,"w")
f = open(file_boolean,"w")
f1.write("")
fp.write("")
f.write("")
for i in range(0,1000):
	fileName = ""
	fileName = fileName + str(i)  
	fileName=fileName+".txt"
	file_content=open(fileName).read()
	tokens=nltk.word_tokenize(file_content)
	f1=open(file_tokenied,'a')
	lenFile=len(tokens) #number of tokens stored here
	for j in range(0,lenFile):
		if (re.match("^[a-zA-Z0-9]*$",tokens[j])and(tokens[j] not in stop)):
			fp.write(tokens[j])
			fp.write("\n")
			f1.write(tokens[j])
			f1.write(" ")
			f1.write(str(i))
			f1.write(" ")
			f1.write(str(j))
			f1.write("\n")
			f.write(tokens[j])
			f.write(" ")
			f.write(str(i))
			f.write("\n")

    
		
    


	
