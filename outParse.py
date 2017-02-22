#Parses the output edge set and dictionary to reconstruct a human-readable edge list.
#Michael Miyagi
#2/21/17

import copy
import numpy
import sys
import json
import re


##http://stackoverflow.com/questions/30226094/how-do-i-decompose-a-number-into-powers-of-2
def pow(x):
	id=[]
	i=1
	counter=0
	while i<=x:
		if i&x:
			id.append(counter)
		counter+=1
		i<<=1
	return id

def readEdges(filepath):
	edgenames=[]
	fp=open(filepath,'r+')
	for line in fp:
	#	print line
		m=re.findall('[0-9]+',line)
		if m:
	#		print m[0],m[1]
			edgenames.append((pow(int(m[0])),pow(int(m[1]))))
#	print edgenames
	return edgenames	
def readKeys(keypath,edgemat):
	keyedEd=[]
	with open(keypath) as df:
		keym=json.load(df)
	for element in edgemat:
	#	print element
		tempPar=[]
		tempChil=[]
		for node in element[0]:
			tempPar.append(keym[node][0])
		for node in element[1]:
			tempChil.append(keym[node][0])
		keyedEd.append((copy.deepcopy(tempPar),copy.deepcopy(tempChil)))
	return keyedEd			

#readEdges(sys.argv[1])
fp=open('./keyedEdges.txt','w')
fp.write(str(readKeys(sys.argv[1],readEdges(sys.argv[2]))))
fp.close()
