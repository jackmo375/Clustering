# import system packages:
import numpy as np

# import local packages:
import simStats as sst
import simPlot as spt
import simGenerate as sgt
import simNetwork as snt

def main():

	# set program constants:
	K = 10	# max number of clusters
	B = 100	# number of null realisations created by gap test
	N = 100	# number of points in the input data cloud

	# generate clusters:
	n1, n2 = 30, 20
	n3 = N - n1 - n2
	cluster_vec = [
		sgt.genCluster((0.3,0.7), 0.1, n1),
		sgt.genCluster((0.1,0.3), 0.1, n2),
		sgt.genCluster((0.7,0.5), 0.1, n3)
	]

	# create data set:
	data_mat = np.concatenate(
		(cluster_vec[0],cluster_vec[1],cluster_vec[2]), 
		axis=0)
	#data_mat = sgt.genPoisson(N)	# uniform point cloud

	# convert data to network:
	dist_mat = snt.getDistanceMatrix(data_mat)

	# perform gap test
	gap_obj = sst.GapTest(K, B).fit(dist_mat)
	spt.plotGapTest(data_mat, gap_obj, fname='../media/gap.png')

if __name__ == '__main__':
	main()