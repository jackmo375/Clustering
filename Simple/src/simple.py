# import local packages:
import simPlot as spt
import simGenerate as sgt

# import system packages:
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def main():

	# fix fake data parameters:
	n1, n2, n3 = 20, 30, 40		# number of points in each cluster
	R1, R2, R3 = 0.1, 0.15, 0.05	# max radius of each cluster

	# generate clusters:
	X1 = sgt.genCluster((0.3,0.8), R1, n1)
	X2 = sgt.genCluster((0.6,0.3), R2, n2)
	X3 = sgt.genCluster((0.8,0.2), R3, n3)

	# create data set:
	n = n1 + n2 + n3	# number of points in fake data set
	X = np.concatenate((X1,X2,X3), axis=0)

	# convert data to network:
	DX = getDistanceMatrix(X)

	# perform clustering on the network:
	#clustering = AgglomerativeClustering(n_clusters=3).fit(X)	# with raw data
	clustering = AgglomerativeClustering(
		n_clusters=3, 
		linkage='average', 
		affinity='precomputed').fit(DX)	# with distance matrix

	# plot it:
	#spt. plotData(X)
	#spt.plotData(X, labels=clustering.labels_)
	spt.plotData(X, labels=clustering.labels_, fName='../media/clusters.pdf')

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


if __name__ == '__main__':
	main()

