# import enviroment modules:
import random as rd
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# import local modules:
import genGenerate as ggt
import genPlot as gpt
import genNetwork as gnt
import genStats as gst

def main():

	# program parameters:
	N_g = 30	# length of each genome in base pairs
	N_p	= 5	# size of pan genome
	K   = 11	# max number of clusters
	B 	= 5

	# generate a genome:	
	#p = ggt.genPanGenome(N_g, N_p*6)
	#p = ggt.genGenomeCluster(N_g, N_p, 30)
	p = np.concatenate((
		ggt.genGenomeCluster(N_g, N_p, 4),
		ggt.genGenomeCluster(N_g, N_p, 4),
		ggt.genGenomeCluster(N_g, N_p, 4),
		ggt.genGenomeCluster(N_g, N_p, 4),
		ggt.genGenomeCluster(N_g, N_p, 4),
		ggt.genGenomeCluster(N_g, N_p, 4)), axis=0)

	dist_mat = gnt.getDistanceMatrix(p)
	print(dist_mat)

	# cluster data:
	clustering = AgglomerativeClustering(
			n_clusters=2, 
			linkage='average', 
			affinity='precomputed').fit(dist_mat)

	#gpt.plotRawPanGenome(p, fname='../media/clusters4.png')

	jump_obj = gst.JumpTest(K,B).fit(dist_mat, N_g)
	gpt.plotJumpTest(p,jump_obj, fname='../media/jump6clusters.png')


if __name__ == '__main__':
	main()