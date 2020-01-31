# Modules
## enviroment:
import sys
import statistics as st
import numpy as np
from sklearn.cluster import AgglomerativeClustering

## local:

class StatsTable:
	# class variables

	# constructor:
	def __init__(self, D):
		'''
		D :: any pairwise distance matrix
		'''
		# instance variables
		self.distances = self._getDistances(D)
		self.max  = max(self.distances)
		self.min  = min(self.distances)
		self.mean = st.mean(self.distances)
		self.sd   = st.stdev(self.distances)

	# class members:
	def _getDistances(self, D):
		# get distinct separation values as a list:
		distances = []
		for i in range(len(D[0,:])):
			for j in range(i):
				distances = distances + [D[i,j]]
		return distances

	def printStatsTable(self, out=sys.stdout):

		out.write('*'*17+'\n')
		out.write('*  Stats table  *\n')
		out.write('*'*17+'\n')
		out.write(
			  f"*  max sep:  {self.max:.2f}\n"
			+ f"*  min sep:  {self.min:.2f}\n"
			+ f"*  mean sep: {self.mean:.2f}\n"
			+ f"*  stdev:    {self.sd:.2f}\n")
		out.write('*'*17+'\n')

class Mapper:
	# class variables:

	# constructor:
	def __init__(self, fmin, fmax, n_sets, epsilon):
		# instance variables:
		self.paramCover = _Cover(fmin, fmax, n_sets, epsilon)

	# class members:
	def fit(self, dist, linkage='single'):
		pass

class _Cover:
	# class variables:

	# class constructor:
	def __init__(self, fmin, fmax, n_sets, epsilon):
		'''
		fmin :: smallest value of filter function applied to data
		fmax :: largest value of filter function applied to data
		n_sets :: number of sets in the cover; index goes from 0 to n_sets-1.
		epsilon :: adjecent sets will overlap by epsilon*Delta_z
		'''
		if (epsilon >= 1.0):
			sys.stderr.write(
				'Warning: at least three sets will overlap\n'
				+ 'in this case, are you sure you want this?\n'
				+ 'n :: no, exit the program\n'
				+ 'y :: continue anyway\n')
			if input("Enter your choice: ") == 'n':
				sys.exit(0)

		# instance variables:
		self.z_0     = fmin
		self.Delta_z = (fmax - fmin)/(n_sets-1)
		self.n_sets  = n_sets
		self.overlap = epsilon*self.Delta_z

	# class members:
	def memberContains(self, value, memIndex):
		'''
		returns True if 'value' is contained in 
		the cover's member set with index memIndex,
		and False otherwise.
		'''
		z_i = self.z_0 + memIndex*self.Delta_z

		if (value > z_i - 0.5*(self.overlap + self.Delta_z)
			and value < z_i + 0.5*(self.overlap + self.Delta_z)):
			return True		
		else:
			return False


#
#	FILTER FUNCTIONS
#
def filterDensity(D, epsilon):
	'''
	D :: pairwise distance matrix
	epsilon :: smoothing parameter
	'''

	n_points = len(D[0,:])

	values = np.zeros([n_points])

	for i in range(n_points):
		for j in range(n_points):
			values[i] += np.exp(-D[i,j]**2/epsilon)

	return values

def filterEccentric(D, p):
	'''
	D :: pairwise distance matrix
	p :: "p-norm" style parameter
	'''

	n_points = len(D[0,:])

	values = np.zeros([n_points])

	for i in range(n_points):
		for j in range(n_points):
			values[i] += D[i,j]**p
		values[i] *= n_points
		values[i] = (values[i])**(1/p)

	return values

def filterLinfinity(D):

	n_points = len(D[0,:])

	values = np.zeros([n_points])

	for i in range(n_points):
		values[i] = max(D[i,:])

	return values




