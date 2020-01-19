import numpy as np
import networkx as nx

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