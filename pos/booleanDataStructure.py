import sys
import nltk
import re

dictWords = []
dictNums = []
dictMixed= [] 
listOfListsNum = []
listOfListWords = []
listOfListMixed = []
temp_list = []

"""file_dictionary = open("dict.txt","r")"""
file_BI=open("booleanInput.txt","r")
"""while 1:
	line=file_dictionary.readline()
	if line == '':
		break
	length = len(line)
	dictionary.append(line[0:length-1])"""

line=file_BI.readline()
tokens=nltk.word_tokenize(line)
first=tokens[0]
file_BI.close()
file_BI=open("booleanInput.txt","r")



while 1:
	line1=file_BI.readline()
	if line1=='':
		break
	tokens1=nltk.word_tokenize(line1)
	if re.match("^[0-9]*$",tokens[j]):
		adsad

    elif re.match("^[a-zA-Z]*$",tokens[j]):
    	asdad
    else :
    	asjdsad

	if tokens1[0]==first:
		temp_list.append(int(tokens1[1]))
	else:
		dictionary.append(first)
		first=tokens1[0]
		temp_list.sort()
		listOfLists.append(temp_list)
		temp_list=[]
		temp_list.append(int(tokens1[1]))

print listOfLists[1]
print len(listOfLists[1])

