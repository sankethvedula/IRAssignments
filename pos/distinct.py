import sys

distinct=open("distinct.txt","w")
distinct.write("")
distinct=open("distinct.txt","w")
mySet=set(line.strip() for line in open("output.txt"))
print mySet
