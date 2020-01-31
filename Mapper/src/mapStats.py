# Modules
## enviroment:
import sys
import statistics as st
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import networkx as nx

## local:
import simStats as sst
import simPlot as spt

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
	def __init__(self, fmin, fmax, n_sets, epsilon, maxclusters, nreals):
		# instance variables:
		self.paramCover   = _Cover(fmin, fmax, n_sets, epsilon)
		self.clusterGraph = nx.Graph()	# initialise grpah to gold the output
		self._subset = []	# container for subsets of data
		self.maxclusters = maxclusters
		self.nreals = nreals

	# class members:
	def fit(self, data, dist, filterValues, linkage='single'):
		
		# loop over sets in the cover:
		for i in range(self.paramCover.n_sets):
			self._subsetData(filterValues, i)
			labels = self._clusterPoints(
				data[self._subset,:],
				dist[self._subset,:][:,self._subset], 
				linkage=linkage)

		self._fillNodeAttributes(filterValues)
		self._fillEdgeList()


	def _subsetData(self, filterValues, memIndex):
		'''
		returns subset of the data: all points such that
		their filter value is in the set with index memIndex 
		in the cover.
			filter :: vector of filter values for each point
			memIndex :: the index of the desired set in the cover
		'''
		
		n_points = len(filterValues)

		# loop over points in the data:
		self._subset = []	# clear subset list
		for i in range(n_points):
			if (self.paramCover.memberContains(
				filterValues[i], 
				memIndex) is True):
				self._subset = self._subset + [i]


	def _clusterPoints(self, data_mat, dist_mat, linkage):

		jump_obj = sst.JumpTest(
			self.maxclusters,
			self.nreals).fit(dist_mat, linkageMethod=linkage)
		spt.plotJumpTest(
			data_mat,
			jump_obj)

		n_clusters = int(input('Estimate number of clusters from the diagram: '))

		# cluster again with optimal number?
		model = AgglomerativeClustering(
			linkage=linkage,
			affinity='precomputed', 
			n_clusters=n_clusters).fit(dist_mat)

		for i in range(n_clusters):
			print(i)
			print(model.labels_)
			pointIDs = [self._subset[j] for j in range(len(model.labels_)) if model.labels_[j]==i]
			print(pointIDs)
			j = self.clusterGraph.number_of_nodes()
			self.clusterGraph.add_node(j, pointIDs=pointIDs, avfvalue=0.0)


	def _fillNodeAttributes(self, filterValues):
		# compute average filter values:
		for i in range(self.clusterGraph.number_of_nodes()):
			pIDs = self.clusterGraph.nodes[i]['pointIDs']
			average = 0.0
			for j in pIDs:
				average += filterValues[j]
			average /= len(pIDs)
			self.clusterGraph.nodes[i]['avfvalue'] = average
			print(self.clusterGraph.nodes[i]['avfvalue'])


	def _fillEdgeList(self):
		for i in range(self.clusterGraph.number_of_nodes()):
			for j in range(i):
				if bool(
					set(self.clusterGraph.nodes[i]['pointIDs']) 
					& set(self.clusterGraph.nodes[j]['pointIDs'])) is True:
					# add edge to graph:
					self.clusterGraph.add_edge(i,j)

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




