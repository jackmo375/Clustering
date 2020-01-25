# Modules
## enviroment:
import numpy as np
from sklearn.cluster import AgglomerativeClustering

## local:
import simGenerate as sgt
import simPlot as spt
import simNetwork as snt
import mapPlot as mpt

def main():

	# generate the data:
	data = np.concatenate((
		sgt.genCluster((0.2,0.2), 0.1, 20),
		sgt.genCluster((0.6,0.7), 0.1, 20),
		sgt.genCluster((0.8,0.2), 0.1, 20)
		),axis=0)

	#data = sgt.genPoisson(60)
	#spt.plotData(data)

	# compute distance matrix:
	dist = snt.getDistanceMatrix(data)

	# cluster the data:
	clustering = AgglomerativeClustering(
		linkage='average',
		affinity='precomputed',
		n_clusters=3).fit(dist)

	# for each cluster, print  cluster and shape histogram:
	#spt.plotData(data, labels=clustering.labels_)
	mpt.plotShapeHist(data, dist, labels=clustering.labels_)

if __name__ == '__main__':
	main()