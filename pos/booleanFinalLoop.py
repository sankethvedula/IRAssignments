import sys
import nltk
import re
from nltk.corpus import stopwords


from bisect import bisect_left
dictWords = []
queryTerms = []
dictNums = []
dictMixed= [] 
templist = []
lnum=[]
llnum=[]
lword=[]
llword=[]
lmixed=[]
llmixed=[]

def binary_search(a, x, lo=0, hi=None):   # can't use a to specify default for hi
    hi = hi if hi is not None else len(a) # hi defaults to len(a)   
    pos = bisect_left(a,x,lo,hi)          # find insertion position
    return (pos if pos != hi and a[pos] == x else -1) 

class PorterStemmer:

    def __init__(self):
        """The main part of the stemming algorithm starts here.
        b is a buffer holding a word to be stemmed. The letters are in b[k0],
        b[k0+1] ... ending at b[k]. In fact k0 = 0 in this demo program. k is
        readjusted downwards as the stemming progresses. Zero termination is
        not in fact used in the algorithm.

        Note that only lower case sequences are stemmed. Forcing to lower case
        should be done before stem(...) is called.
        """

        self.b = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.j = 0   # j is a general offset into the string

    def cons(self, i):
        """cons(i) is TRUE <=> b[i] is a consonant."""
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        if self.b[i] == 'y':
            if i == self.k0:
                return 1
            else:
                return (not self.cons(i - 1))
        return 1

    def m(self):
        """m() measures the number of consonant sequences between k0 and j.
        if c is a consonant sequence and v a vowel sequence, and <..>
        indicates arbitrary presence,

           <c><v>       gives 0
           <c>vc<v>     gives 1
           <c>vcvc<v>   gives 2
           <c>vcvcvc<v> gives 3
           ....
        """
        n = 0
        i = self.k0
        while 1:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i = i + 1
            i = i + 1

    def vowelinstem(self):
        """vowelinstem() is TRUE <=> k0,...j contains a vowel"""
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0

    def doublec(self, j):
        """doublec(j) is TRUE <=> j,(j-1) contain a double consonant."""
        if j < (self.k0 + 1):
            return 0
        if (self.b[j] != self.b[j-1]):
            return 0
        return self.cons(j)

    def cvc(self, i):
        """cvc(i) is TRUE <=> i-2,i-1,i has the form consonant - vowel - consonant
        and also if the second c is not w,x or y. this is used when trying to
        restore an e at the end of a short  e.g.

           cav(e), lov(e), hop(e), crim(e), but
           snow, box, tray.
        """
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i-1) or not self.cons(i-2):
            return 0
        ch = self.b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends(self, s):
        """ends(s) is TRUE <=> k0,...k ends with the string s."""
        length = len(s)
        if s[length - 1] != self.b[self.k]: # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k-length+1:self.k+1] != s:
            return 0
        self.j = self.k - length
        return 1

    def setto(self, s):
        """setto(s) sets (j+1),...k to the characters in the string s, readjusting k."""
        length = len(s)
        self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
        self.k = self.j + length

    def r(self, s):
        """r(s) is used further down."""
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        """step1ab() gets rid of plurals and -ed or -ing. e.g.

           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat

           feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess

           meetings  ->  meet
        """
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):   self.setto("ate")
            elif self.ends("bl"): self.setto("ble")
            elif self.ends("iz"): self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

    def step1c(self):
        """step1c() turns terminal y to i when there is another vowel in the stem."""
        if (self.ends("y") and self.vowelinstem()):
            self.b = self.b[:self.k] + 'i' + self.b[self.k+1:]

    def step2(self):
        """step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """
        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):   self.r("ate")
            elif self.ends("tional"):  self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):      self.r("ence")
            elif self.ends("anci"):    self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):       self.r("ble") # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):    self.r("al")
            elif self.ends("entli"):   self.r("ent")
            elif self.ends("eli"):     self.r("e")
            elif self.ends("ousli"):   self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):   self.r("ize")
            elif self.ends("ation"):   self.r("ate")
            elif self.ends("ator"):    self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):     self.r("al")
            elif self.ends("iveness"): self.r("ive")
            elif self.ends("fulness"): self.r("ful")
            elif self.ends("ousness"): self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):     self.r("al")
            elif self.ends("iviti"):   self.r("ive")
            elif self.ends("biliti"):  self.r("ble")
        elif self.b[self.k - 1] == 'g': # --DEPARTURE--
            if self.ends("logi"):      self.r("log")
        # To match the published algorithm, delete this phrase

    def step3(self):
        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""
        if self.b[self.k] == 'e':
            if self.ends("icate"):     self.r("ic")
            elif self.ends("ative"):   self.r("")
            elif self.ends("alize"):   self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):      self.r("ic")
            elif self.ends("ful"):     self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
        if self.b[self.k - 1] == 'a':
            if self.ends("al"): pass
            else: return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"): pass
            elif self.ends("ence"): pass
            else: return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"): pass
            else: return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"): pass
            else: return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"): pass
            elif self.ends("ible"): pass
            else: return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"): pass
            elif self.ends("ement"): pass
            elif self.ends("ment"): pass
            elif self.ends("ent"): pass
            else: return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'): pass
            elif self.ends("ou"): pass
            # takes care of -ous
            else: return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"): pass
            else: return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"): pass
            elif self.ends("iti"): pass
            else: return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"): pass
            else: return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"): pass
            else: return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"): pass
            else: return
        else:
            return
        if self.m() > 1:
            self.k = self.j

    def step5(self):
        """step5() removes a final -e if m() > 1, and changes -ll to -l if
        m() > 1.
        """
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k-1)):
                self.k = self.k - 1
        if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k = self.k -1

    def stem(self, p, i, j):
        """In stem(p,i,j), p is a char pointer, and the string to be stemmed
        is from p[i] to p[j] inclusive. Typically i is zero and j is the
        offset to the last character of a string, (p[j+1] == '\0'). The
        stemmer adjusts the characters p[i] ... p[j] and returns the new
        end-point of the string, k. Stemming never increases word length, so
        i <= k <= j. To turn the stemmer into a module, declare 'stem' as
        extern, and delete the remainder of this file.
        """
        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b # --DEPARTURE--

        # With this line, strings of length 1 or 2 don't go through the
        # stemming process, although no mention is made of this in the
        # published algorithm. Remove the line to match the published
        # algorithm.

        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.b[self.k0:self.k+1]

def buildIndex():
	templist = []
	 
	file_BI=open("booleanInput.txt","r")
	i = 0
	while 1:
		i = i + 1
		print i
		line1=file_BI.readline()
		if line1=='':
			break
		tokens1=nltk.word_tokenize(line1)
		if  re.match("^[0-9]*$",tokens1[0]):
			templist.append(tokens1[0])
			templist.append(int(tokens1[1]))
			dictNums.append(templist)
			templist=[]
		elif re.match("^[a-zA-Z]*$",tokens1[0]):
			templist.append(tokens1[0])
			templist.append(int(tokens1[1]))
			dictWords.append(templist)
			templist=[]
		else:
			templist.append(tokens1[0])
			templist.append(int(tokens1[1]))
			dictMixed.append(templist)
			templist=[]



	dictWords.sort()
	dictMixed.sort()
	dictNums.sort(key=lambda x: int(x[0]))

	lengthNumberDic = len(dictNums)
	lengthWordDic = len(dictWords)
	lengthMixedDic = len(dictMixed)

	first=dictWords[0][0]
	for i in range(0,lengthWordDic):
		if(first==dictWords[i][0]):
			templist.append(dictWords[i][1])
		else:
			lword.append(first)
			first=dictWords[i][0]
			templist.sort()
			llword.append(templist)
			templist=[]
			templist.append(dictWords[i][1])

	first=dictNums[0][0]
	templist=[]
	for i in range(0,lengthNumberDic):
		if(first==dictNums[i][0]):
			templist.append(dictNums[i][1])
		else:
			lnum.append(first)
			first=dictNums[i][0]
			templist.sort()
			llnum.append(templist)
			templist=[]
			templist.append(dictNums[i][1])

	first=dictMixed[0][0]
	templist=[]
	for i in range(0,lengthMixedDic):
		if(first==dictMixed[i][0]):
			templist.append(dictMixed[i][1])
		else:
			lmixed.append(first)
			first=dictMixed[i][0]
			templist.sort()
			llmixed.append(templist)
			templist=[]
			templist.append(dictMixed[i][1])

if __name__ == "__main__":
	
	queryTerms = []
	stop=stopwords.words('english')


	buildIndex()

	
	p = PorterStemmer()
while 1:
    print "Entered query loop\n"
    output = ''
    word = ''
    line = raw_input("Enter the query\n")
    line = line + " "
    line_tokens_revised = nltk.word_tokenize(line)
    wildCardTokens = []
    for wildcard in line_tokens_revised:
    	if "*" in wildcard:
    		wildCardTokens.append(wildcard)
    		line_tokens_revised.remove(wildcard)
    #wildCardQuery = 
    wildLists = []
    for wildcard in wildCardTokens:
    	wildIndex = wildcard.index("*")
    	i =0
    	if wildIndex > 0 :
    		wildPart = wildcard[0:wildIndex]
    		
    		for words in lword:
    			if words.startswith(wildPart):
    				print words
    				wildLists.append(llword[i])
    				i = i +1

    	else:
    		wildPart = wildcard[1:]
    		for words in lword:
    			if words.endswith(wildPart):
    				print words
    				wildLists.append(llword[i])
    				i = i +1


    print len(wildLists)
    print wildLists
    i = 0
    words = ""		
    removed_tokens = []
    nonremoved_tokens = []
    for term2 in line_tokens_revised:
        if re.match("^[a-zA-Z]*$",term2):
            nonremoved_tokens.append(term2)
        elif re.match("^[0-9]*$",term2):
            removed_tokens.append(term2)
        else:
            removed_tokens.append(term2)
    line_revised = ''
    for term3 in nonremoved_tokens:
        line_revised = line_revised + term3 + " "
    if line == "q ":
        print "exiting AnyDayBetterThanGoogle"
        break

    for c in line_revised:
        if c.isalpha():
            print c
            word += c.lower()
        else:
            if word:
                output += p.stem(word,0,len(word)-1)
                word =''
                output += c.lower()
                print output
    lineTokens=nltk.word_tokenize(line)
    for term1 in removed_tokens:
        output=output + " " + term1
    queryTerms = nltk.word_tokenize(output)
    print queryTerms
    queryll = []                                                               # queryll is list of postinglists of query terms.
    templist = []                                                              # storing the posting list temporarily in each case and finally appending to queryll
    null = []                                                                  # push null if the term doesn't exist in the vocabulary
    print "entering the query execution process...\n"
    for term in queryTerms:
        print "Entered a term..\n"
        
        if (re.match("^[a-zA-Z0-9]*$",term)and(term not in stop)):
            if re.match("^[0-9]*$",term):
                indices = [i for i, x in enumerate(lnum) if x == term]
                length_indices = len(indices)
                for i in range(0,length_indices):
                    for j in range(0,len(llnum[indices[i]])):
                        templist.append(llnum[indices[i]][j])
                    
                
                templist.sort()
                print templist
                queryll.append(templist)
            elif re.match("^[a-zA-Z]*$",term):
                try:
                    index1 = lword.index(term)
                    print len(llword[index1])
                    queryll.append(llword[index1])
                except ValueError:
                    queryll.append(null)
                #if index1>0:
                    
            else:
                try:
                   index1 = lmixed.index(term)
                   print len(llmixed[index1])
                   queryll.append(llmixed[index1])

                except ValueError:
                    queryll.append(null)
                #if index1 > 0:
    postingLists = len(queryll)                                             # length of queryll
    i =0                                                                    # pointer of 1st posting list
    j =0                                                                    # pointer of 2nd posting list
    temp_post = []                                                          # temporarily stores the intersection(LOGICAL AND) of posting lists 1 and 2
    if  postingLists <= 1:
        print queryll
        continue

    while i < len(queryll[0]) and j < len(queryll[1]):
        if queryll[0][i] == queryll[1][j]:
            temp_post.append(queryll[0][i])
            i+=1
            j+=1
        elif queryll[0][i] < queryll[1][j]:
            i+=1
        else:
            j+=1
   
    k=0
    for k in range(2,postingLists):
        rewrite=0
        i=0
        j=0
        while i < len(temp_post) and j < len(queryll[k]):
            if temp_post[i] == queryll[k][j]:
                temp_post[rewrite]=temp_post[i]
                rewrite+=1
                i+=1
                j+=1
            elif temp_post[i] < queryll[k][j]:
                i+=1
            else:
                j+=1
        del temp_post[rewrite:len(temp_post)]
    print temp_post







                    


#for i in range (0,queryLen):'''	# query processing start 
