# Modules
## enviroment:
import numpy as np
import sys

## local:
import genGenerate as ggt
import genPlot as gpt
import genNetwork as gnt
from sklearn.cluster import AgglomerativeClustering

def main():

	N_g = 30	# length of each genome in base pairs
	N_p	= 5	# size of pan genome

	# generate data:
	p = np.concatenate((
		ggt.genGenomeCluster(N_g, N_p, 4),
		ggt.genGenomeCluster(N_g, N_p, 4),
		ggt.genGenomeCluster(N_g, N_p, 4),
		ggt.genGenomeCluster(N_g, N_p, 4),
		ggt.genGenomeCluster(N_g, N_p, 4),
		ggt.genGenomeCluster(N_g, N_p, 4)), axis=0)

	# cluster:
	dist_mat = gnt.getDistanceMatrix(p)
	clustering = AgglomerativeClustering(
			n_clusters=6, 
			linkage='average', 
			affinity='precomputed').fit(dist_mat)

	# print:
	folder = '../media/'
	label = sys.argv[1]
	gpt.plotRawPanGenome(p, fname=folder+label+'1.png', show=False)
	gpt.plotClustersGraph(clustering.labels_, fname=folder+label+'2.png')

if __name__ == '__main__':
	main()