import random as rd
import numpy as np

def genCluster(c, R, n):
	'''
	Generate a cluster with:
		c :: center (two element tuple)
		R :: max radius(positive float)
		n :: number of points (positive int)
	'''
	points = np.empty([n,2])
	for i in range(n):
		r = rd.uniform(0, R)
		theta = rd.uniform(0, 2*np.pi)
		point = np.array([
			r*np.cos(theta) + c[0],
			r*np.sin(theta) + c[1]])
		points[i] = point
	
	return points

def genClusters(c_vec, R_vec, n_vec):

	cluster_tup = tuple([genCluster(c_vec[i], R_vec[i], n_vec[i]) for i in range(len(c_vec))])

	return np.concatenate(cluster_tup, axis=0)

def genPoisson(n):
	'''
	generate uniform random point cloud
	over [0,1]^2
		n :: number of points
	'''
	points = np.empty([n,2])
	for i in range(n):
		point = np.array([
			rd.uniform(0,1),
			rd.uniform(0,1)])
		points[i] = point

	return points

# non-globular clusters
def genAnnulusCluster(c, R1, R2, n):
	'''
	Generate an annulus cluster of points in [0,1]^2 with:
		c :: ring center
		R1 :: inner radius
		R2 :: outer radius
	'''
	points = np.empty([n,2])
	for i in range(n):
		r = rd.uniform(R1, R2)
		theta = rd.uniform(0, 2*np.pi)
		point = np.array([
			r*np.cos(theta) + c[0],
			r*np.sin(theta) + c[1]])
		points[i] = point

	return points

