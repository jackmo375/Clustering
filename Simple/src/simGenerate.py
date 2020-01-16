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