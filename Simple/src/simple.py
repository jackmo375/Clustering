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
import sys

def main():

	# generate clusters:
	data_mat = np.concatenate((
		sgt.genCluster((0.2,0.5), 0.15, 6),
		sgt.genCluster((0.6,0.7), 0.15, 5),
		sgt.genCluster((0.7,0.2), 0.15, 3)),
		axis=0)

	# convert data to network:
	dist_mat = snt.getDistanceMatrix(data_mat)
	#GX = snt.graphFromDistMatrix(DX)

	# perform clustering on the network:
	#clustering = AgglomerativeClustering(n_clusters=3).fit(X)	# with raw data
	clustering = AgglomerativeClustering(
		n_clusters=3, 
		linkage='average', 
		affinity='precomputed').fit(dist_mat)	# with distance matrix

	# plot it:
	#spt.plotData(X, annotate=True)
	#spt.plotData(X, labels=clustering.labels_)
	#spt.plotData(X, labels=clustering.labels_, fName='../media/clusters.pdf')
	#spt.plotGraph(GX)

	#spt.plotData(X, fName="../media/pointCloud.png")
	#spt.plotClustersGraph(clustering.labels_, fname='../media/clusters.graph.png')
	#spt.plotPointsGraph(X)

	spt.plotClustersAndGraph(data_mat,clustering.labels_, ffolder='../media/', flabel=sys.argv[1])

if __name__ == '__main__':
	main()

