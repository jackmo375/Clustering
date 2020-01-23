# import enviroment modules:
import numpy as np
from scipy.spatial.distance import hamming

# import local modules:


def getDistanceMatrix(panGenome, metric='hamming'):

	n_p = len(panGenome[:,0])
	dist_mat = np.zeros([n_p,n_p]) # initialized pan genome distance matrix
	for i in range(n_p):
		for j in range(i):
			dist_mat[i,j] = hamming(panGenome[i],panGenome[j])
	for i in range(n_p):
		for j in range(i+1,n_p):
			dist_mat[i,j] = dist_mat[j,i]
			
	return dist_mat