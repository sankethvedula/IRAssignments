import nltk
import sys


i = 0
file_tokenied="tokenized.txt"
file_porter="porterWords.txt"
f1=open(file_tokenied,"w")
fp=open(file_porter,"w")
f1.write("")
fp.write("")
for i in range(0,1000):
	fileName = ""
	fileName = fileName + str(i)  
	fileName=fileName+".txt"
	file_content=open(fileName).read()
	tokens=nltk.word_tokenize(file_content)
	f1=open(file_tokenied,'a')
	lenFile=len(tokens) #number of tokens stored here
	for j in range(0,lenFile):
		fp.write(tokens[j])
		fp.write("\n")
		f1.write(tokens[j])
		f1.write(" ")
		f1.write(str(i))
		f1.write(" ")
		f1.write(str(j))
		f1.write("\n")
    
    


	