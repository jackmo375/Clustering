# Modules #
## enviroment:
import numpy as np
from sklearn.cluster import AgglomerativeClustering

## local:
import genNetwork as gnt
import genGenerate as ggt

class JumpTest:
	'''
	Gap test adapted to dendrogram representation
	of hiearchical clustering procedures.
	The visual part works very well in selecting the
	true number of clusters, but the test is wrong
	most times. Need to either fix it, or ignore it. 	
		w :: dendrogram node height
	'''
	# class variables:

	# constructor:
	def __init__(self, maxclusters, nreals):
		# instance variables:
		self.maxclusters = maxclusters
		self.nreals = nreals
		self.linkage_mat = []
		self.w_log_vec = np.empty([maxclusters])
		self.wnull_log_average_vec = np.empty([maxclusters])

	# class members:
	def fit(self, dist_mat, n_g, linkageMethod='average'):

		n_p = len(dist_mat[:,0])

		# compute data dendrogram:
		model = AgglomerativeClustering(
			linkage=linkageMethod,
			affinity='precomputed',
			distance_threshold=0, 
			n_clusters=None).fit(dist_mat)
		self.linkage_mat = get_linkage_matrix(model)

		p = self.maxclusters+1
		distances = self.linkage_mat[:,2][:-p:-1]
		self.w_log_vec = np.log10(distances)

		# generate realisations:
		wnull_log_mat = np.empty([self.maxclusters,self.nreals])
		for b in range(self.nreals):
			distnull_mat = gnt.getDistanceMatrix(ggt.genPanGenome(n_g, n_p))
			model = AgglomerativeClustering(
				linkage='average',
				affinity='precomputed',
				distance_threshold=0, 
				n_clusters=None).fit(distnull_mat)
			self.null_linkage_mat = get_linkage_matrix(model)
			distances = self.null_linkage_mat[:,2][:-p:-1]
			wnull_log_mat[:,b] = np.log10(distances)

		self.wnull_log_average_vec = wnull_log_mat.mean(1)
		self.wnull_log_err_vec = wnull_log_mat.var(1) \
			*(1 + 1/self.nreals)**0.5

		self.gap = self.wnull_log_average_vec - self.w_log_vec

		# estimate optimal k:
		for i in range(self.maxclusters-1):
			if self.gap[i] >= self.gap[i+1] - self.wnull_log_err_vec[i+1]:
				print(f"optimal k: {i+1}")
				break

		return self

def get_linkage_matrix(model):
	'''
	Authors: Mathew Kallada, Andreas Mueller
	License: BSD 3 clause
	taken from: https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html
	'''
	# Create linkage matrix and then plot the dendrogram

	# create the counts of samples under each node
	counts = np.zeros(model.children_.shape[0])
	n_samples = len(model.labels_)
	for i, merge in enumerate(model.children_):
		current_count = 0
		for child_idx in merge:
			if child_idx < n_samples:
				current_count += 1  # leaf node
			else:
				current_count += counts[child_idx - n_samples]
		counts[i] = current_count

	return np.column_stack([model.children_, model.distances_,
										counts]).astype(float)