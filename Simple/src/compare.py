# import enviroment modules:
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# import local modules:
import simGenerate as sgt
import simPlot as spt
import simNetwork as snt
import simStats as sst

def main():

	N = 200
	K = 10
	B = 5

	# generate fake data
	data_mat = np.concatenate((
		sgt.genAnnulusCluster((0.5, 0.5), 0.4, 0.3, N),
		sgt.genCluster((0.5,0.5), 0.1, 100)),
		axis=0)

	# get distance matrix:
	dist_mat = snt.getDistanceMatrix(data_mat)

	# cluster it
	clustering = AgglomerativeClustering(
		n_clusters=2,
		linkage='single',
		affinity='precomputed').fit(dist_mat)
	#elb_obj = sst.ElbowTest(K).fit(dist_mat, linkage='single')
	jump_obj = sst.JumpTest(K,B).fit(dist_mat, linkageMethod='single')


	# plot it:
	#spt.plotData(data_mat, labels=clustering.labels_, fname='../media/ring.singleLink1.png')
	#spt.plotElbowTest(data_mat, elb_obj)
	spt.plotJumpTest(data_mat, jump_obj, fname='../media/jumpRing.png')

if __name__ == '__main__':
	main()