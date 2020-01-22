# import enviroment modules:

# import local modules:
import simNetwork as snt
import simPlot as spt
import simGenerate as sgt
import simStats as sst

def main():
    # set program constants:
	K = 10  # max number of clusters
	B = 100 # number of null realisations created by gap test
	N = 100 # number of points in the input data cloud

	# fake data parameters:
	n_vec = [20, 40, 20]
	n_vec = n_vec + [N - sum(n_vec)]
	radii_vec = [0.1]*4
	center_vec = [(0.3,0.7), (0.1,0.3), (0.5,0.1), (0.8,0.5)]

	# generate data:
	#data_mat = sgt.genClusters(center_vec, radii_vec, n_vec)
	data_mat = sgt.genPoisson(N)   # uniform point cloud

    # convert data to network:
	dist_mat = snt.getDistanceMatrix(data_mat)

	jump_obj = sst.JumpTest(K,B).fit(dist_mat)

    # plot the top p levels of the dendrogram
	spt.plotJumpTest(
		data_mat,
		jump_obj, 
		fname='../media/jump2.png')

if __name__ == '__main__':
	main()