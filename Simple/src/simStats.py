# import enviroment packages:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as st
from sklearn.cluster import AgglomerativeClustering

# import local packages:
import simNetwork as snt

class ElbowTest:
	# class variables

	# constructor
	def __init__(self, maxclusters):
		# instance variables:
		self.maxclusters = maxclusters       # max number of clusters
		self.w_vec = np.empty([maxclusters])

	# class members
	def fit(self, dist_mat):
		self.w_vec = elbowTest(dist_mat, self.maxclusters)
		return self


class GapTest:
	'''
	w :: within-cluster dispersion
	'''
	# class variables:

	# constructor:
	def __init__(self, maxclusters, nreals):
		# instance varianbles:
		self.maxclusters = maxclusters  # max number of clusters
		self.nreals      = nreals	  		# number of independent realisations of null model to draw
		self.w_log_vec 		 = np.empty([maxclusters])
		self.wnull_log_average_vec = np.empty([maxclusters])
		self.wnull_log_err_vec = np.empty([maxclusters])
		self.gap = np.empty([maxclusters])

	# class members:
	def fit(self, dist_mat):

		npoints = len(dist_mat[:,0])

		self.w_log_vec = np.log10(elbowTest(dist_mat, self.maxclusters))

		wnull_log_mat = np.zeros([self.maxclusters,self.nreals])
		for b in range(self.nreals):
			wnull_log_mat[:,b] = np.log10(
				elbowTest(
					snt.randomDistanceMatrix(npoints), 
					self.maxclusters))
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


def elbowTest(D, maxNClusters):
	'''
	outputs elbow test graph (via plt.show())
	'''

	nPoints = len(D[:,0])

	# compute total variance:
	pointSeps = np.array([])	# initialized list of point separations
	for i in range(nPoints):
		for j in range(i):
			pointSeps = np.append(pointSeps, [D[i,j]])
	totalVar = st.variance(pointSeps)

	# compute unexplained variance for increasing nClusters:
	unexVar = []
	for k in range(1, maxNClusters+1):
		# get clustering labels:
		clustering = AgglomerativeClustering(
			n_clusters=k, 
			linkage='average', 
			affinity='precomputed').fit(D)
		# find A
		A = []
		for i in range(nPoints):
			for j in range(i):
				if clustering.labels_[i] == clustering.labels_[j]:
					A = A + [D[i,j]]

		if len(A) <= 1:
			maxNClusters = k-1
			break

		Avar = st.variance(A)
		unexVar = unexVar + [Avar]

	return unexVar