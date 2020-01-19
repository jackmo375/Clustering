# import local packages:
import simPlot as spt
import simGenerate as sgt
import simStats as sst
import simNetwork as snt

# import system packages:
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import networkx as nx

def main():

	# fix fake data parameters:
	n1, n2, n3 = 6, 5, 6		# number of points in each cluster
	R1, R2, R3 = 0.1, 0.1, 0.1	# max radius of each cluster

	# generate clusters:
	X1 = sgt.genCluster((0.3,0.7), R1, n1)
	X2 = sgt.genCluster((0.1,0.3), R2, n2)
	X3 = sgt.genCluster((0.7,0.5), R3, n3)

	# create data set:
	n = n1 + n2 + n3	# number of points in fake data set
	X = np.concatenate((X1,X2,X3), axis=0)

	# convert data to network:
	DX = snt.getDistanceMatrix(X)
	GX = snt.graphFromDistMatrix(DX)


	# perform clustering on the network:
	#clustering = AgglomerativeClustering(n_clusters=3).fit(X)	# with raw data
	clustering = AgglomerativeClustering(
		n_clusters=3, 
		linkage='average', 
		affinity='precomputed').fit(DX)	# with distance matrix

	# plot it:
	#spt.plotData(X)
	#spt.plotData(X, labels=clustering.labels_)
	#spt.plotData(X, labels=clustering.labels_, fName='../media/clusters.pdf')
	#spt.plotGraph(GX)

	spt.plotData(X, fName="../media/pointCloud.png")
	spt.plotClustersGraph(clustering.labels_)
	spt.plotPointsGraph(X)

if __name__ == '__main__':
	main()

