import numpy as np
import networkx as nx
import random as rd

# import enviroment packages:
import simGenerate as sgt

def getDistanceMatrix(X):
	'''
	Gets distance matrix from a list, X, of points in R^2
		+ X must be a numpy [n,2] matrix, for n points 
	'''
	n = len(X[:,0])
	D = np.zeros([n,n]) # initialized distance matrix of X
	for i in range(n):
		for j in range(i):
			D[i,j] = np.linalg.norm(X[i,:] - X[j,:])	# Euclidean norm
	for i in range(n):
		for j in range(i+1,n):
			D[i,j] = D[j,i]
	return D

def _permutateDistMatrix(D):
	'''
	create random permutation of input distance matrix
	(this function probably belongs in simNetwork, not here)
	'''
	nPoints = len(D[:,0])

	stack = []
	for i in range(nPoints):
		for j in range(i):
			stack = stack + [(i,j)]

	permStack = []
	while stack != []:
		# select random element from stack:
		i = rd.randint(0,len(stack)-1)
		# pull from stack and add to permStack:
		permStack = permStack + [stack.pop(i)]

	permD = np.zeros([nPoints,nPoints]) # initialized distance matrix of X
	for i in range(nPoints):
		for j in range(i):
			permD[i,j] = D[permStack[i+j]]
	for i in range(nPoints):
		for j in range(i+1,nPoints):
			permD[i,j] = permD[j,i]
	
	return permD

def randomDistanceMatrix(nPoints):

	X = sgt.genPoisson(nPoints)

	return getDistanceMatrix(X)


def getSubGraphs(G, clusterLabels):
	'''
	Returns a list of subgraphs of G, using
	set of cluster labels
		+ G must be networkx graph
		+ ...
	'''
	nClusters = max(clustering.labels_)

	subGraphNodes = []
	for i in range(nClusters+1):
		subGraphNodes = subGraphNodes + [[]]
	for i in range(n):
		j = clustering.labels_[i]
		subGraphNodes[j] = subGraphNodes[j] + [i]
		print(j)
	print(subGraphNodes)
	subGraphs = []
	for nodeSet in subGraphNodes:
		print(nodeSet)
		subGraphs = subGraphs + [nx.subgraph(G,nodeSet)]

	return subGraphs

def graphFromDistMatrix(D):
	n = len(D[:,0])
	G = nx.complete_graph(n)
	# weight graph edges with pairwise distances:
	for i in range(n):
		for j in range(i):
			G.edges[i,j]['weight'] = D[i,j]
	return G