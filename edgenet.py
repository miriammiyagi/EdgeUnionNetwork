#Tree Edge Union Network Construction Script
#by Michael Miyagi
#Last edited on 12/31/16
#Required packages: ETE, NetworkX

import numpy as np
import networkx as nx
import sys
from ete3 import Tree
import glob
import re

removaltracker=0
edgecounter=0
numtrees=0

def cleanComments(filepath):
	for item in glob.glob(filepath):
		with open(item, 'r+') as tf:
			text=tf.read()
			temp=re.sub("[\[].*?[\]]","",text)
			tf.seek(0)
			tf.write(temp)
			tf.truncate()
			tf.close()

def multi_new(filepath):
	returnlist=[]
	f= open(filepath).read()
	composite=f.split(';')
	for item in composite:
#		item=item.strip()
		if item.strip():
			#print "'",item,"'"
			#print len(item)
			returnlist.append((item+';').strip('\n'))
#	print returnlist
	return returnlist

def inputSet(filepath):
	global numtrees
	G=nx.DiGraph()
	print glob.glob(filepath)
	d = {}
	t=Tree(multi_new(glob.glob(filepath)[0])[0])
	leaflist=t.get_leaf_names()
	for index,leaf in enumerate(leaflist):
		d[leaf]=2**index
	for fileitem in glob.glob(filepath):
		for item in multi_new(fileitem):
			numtrees+=1
			t=Tree(item)
			tree_dfs(t.get_tree_root(),sum(d.values()),len(d),G,d)
	nx.set_node_attributes(G,'seen',False)
	return G

def tree_dfs(node,nodesum,nodecount,network,d):
	global edgecounter
	for child in list(node.children):
		endsum=0
		counter=0
		for name in child.get_leaf_names():
			endsum+=d[name]
			counter+=1
		network.add_edge(nodesum,endsum,size=counter-nodecount)
		edgecounter+=1
		tree_dfs(child,endsum,counter,network,d)

def pruneNet(network):
	global removaltracker
	for e in network.edges():
		if ne_dfs(e[0],False,network[e[0]][e[1]]['size'],0,network,e[0],e[1]):
			removaltracker+=1
			network.remove_edge(e[0],e[1])
		nx.set_node_attributes(network,'seen',False)
	print 'networkedges: ',len(network.edges())
	return network.edges()

def ne_dfs(pri,readyflag,boundary,lengthtot,network,start,goal):
	if start==goal:
		return False
	else:
		network.node[start]['seen']=True
	if not network.successors(start):
		return False
	else:
		for item in (network.successors(start)):
			if start==pri:
				readyflag=False
			if not (network.node[item]['seen']):
				if network[start][item]['size']<=boundary-lengthtot and item|goal==goal:
					if goal==item and readyflag:
						return True
				readyflag=True
				if ne_dfs(pri,readyflag,boundary,lengthtot+network[start][item]['size'],network,item,goal):
					return True
	return False

cleanComments(sys.argv[1])
pruneNet(inputSet(sys.argv[1]))
print 'edges: ', edgecounter
print 'trees: ', numtrees
print 'removed: ',removaltracker
