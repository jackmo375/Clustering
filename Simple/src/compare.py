# import enviroment modules:
import numpy as np

# import local modules:
import simGenerate as sgt
import simPlot as spt
import simNetwork as snt
import simStats as sst

def main():

	N = 200
	K = 10

	# generate fake data
	n_vec = [20, 40, 20]
	n_vec = n_vec + [N - sum(n_vec)]

	data_mat = np.concatenate((
		sgt.genAnnulusCluster((0.5, 0.5), 0.4, 0.3, N),
		sgt.genCluster((0.5,0.5), 0.1, 30)),
		axis=0)

	# get distance matrix:
	dist_mat = snt.getDistanceMatrix(data_mat)

	# cluster it
	elb_obj = sst.ElbowTest(K).fit(dist_mat, linkage='single')

	# plot it:
	#spt.plotData(data_mat)
	spt.plotElbowTest(data_mat, elb_obj)

if __name__ == '__main__':
	main()