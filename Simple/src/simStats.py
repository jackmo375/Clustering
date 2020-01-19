# import enviroment packages:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as st

from sklearn.cluster import AgglomerativeClustering


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

	return range(1, maxNClusters+1), unexVar