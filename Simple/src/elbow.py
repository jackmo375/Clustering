# import local packages:
import simGenerate as sgt
import simPlot as spt
import simNetwork as snt
import simStats as sst

# import enviroment packages:
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def main():

	K = 10	# max number of clusers

	# fix fake data parameters:
	n1, n2, n3 = 30, 20, 15		# number of points in each cluster
	R1, R2, R3 = 0.3, 0.1, 0.1	# max radius of each cluster

	# generate clusters:
	X1 = sgt.genCluster((0.3,0.7), R1, n1)
	X2 = sgt.genCluster((0.1,0.3), R2, n2)
	X3 = sgt.genCluster((0.7,0.5), R3, n3)

	# create data set:
	n = n1 + n2 + n3	# number of points in fake data set
	X = np.concatenate((X1,X2,X3), axis=0)
	#X = sgt.genPoisson(n)	# uniform point cloud

	# convert data to network:
	dist_mat = snt.getDistanceMatrix(X)

	# perform elbow test:
	elbow_obj = sst.ElbowTest(K).fit(dist_mat)
	spt.plotElbowTest(X, elbow_obj, fname='../media/elbow.png')


if __name__ == '__main__':
	main()