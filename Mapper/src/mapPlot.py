# Modules
## enviroment:
import matplotlib.pyplot as plt
import matplotlib.cm as cm 	# for color maps
import matplotlib.colors as co
import networkx as nx

from matplotlib import rcParams
rcParams['axes.linewidth'] = 2.5 # set the value globally
rcParams['axes.edgecolor'] = 'grey'
rcParams["figure.figsize"] = [10,10]
rcParams['xtick.labelsize'] = 15
rcParams['ytick.labelsize'] = 15
rcParams['xtick.color'] = 'grey'
rcParams['ytick.color'] = 'grey'
rcParams['lines.linewidth'] = 2.5
rcParams['axes.labelsize'] = 15
rcParams['axes.labelcolor'] = 'grey'


def plotPoints(data, labels=None, fname=None, show=True):

	fig, ax = plt.subplots(1,1, figsize=(10,10))

	_plotPointCloud(data, ax, labels=labels)

	plt.tight_layout()

	# save figure:
	if fname is not None:
		plt.savefig(fname)

	if show is True:
		plt.show()

def plotShapeHist(data, D, labels=None, fname=None, show=True):

	n_points = len(D[:,0])
	if labels is None:
		labels = [0]*n_points
	n_clusters = max(labels)+1

	# generate n_clusters x 2 subplots:
	nrows = 2
	if n_clusters == 1:
		ncols = 1
	else:
		ncols = 1 + n_clusters
	fig, axes = plt.subplots(
		nrows=nrows, 
		ncols=ncols, 
		figsize=(5*ncols,5*nrows))

	if n_clusters == 1:
		_plotPointsAndHist(data, D, axes[0], axes[1])
	else:
		_plotPointsAndHist(data, D, axes[0,0], axes[1,0])
		for i in range(n_clusters):
			# compute index set for cluster i:
			A = []
			for j in range(len(labels)):
				if labels[j] == i:
					A = A + [j]
			_plotPointsAndHist(data[A,:], D[A,:][:,A], axes[0,i+1], axes[1,i+1])

	plt.tight_layout()

	# save figure:
	if fname is not None:
		plt.savefig(fname)

	if show is True:
		plt.show()


def plotPointsFilterHist(data, filter, fname=None, show=True):

	fig, axes = plt.subplots(1,2, figsize=(10,5))

	_plotPointCloud(data, axes[0], labels=filter)
	axes[1].hist(filter)
	axes[1].set_xlabel('filter value')

	plt.tight_layout()

	# save figure:
	if fname is not None:
		plt.savefig(fname)

	if show is True:
		plt.show()


def plotGraph(G, fname, colorAtt=None):

	# print it:
	A = nx.nx_agraph.to_agraph(G)

	n_nodes = G.number_of_nodes()
	n_edges = G.number_of_edges()

	if colorAtt is not None:
		# get node attribute vaues as a list:
		nodeValues = []
		for i in range(n_nodes):
			nodeValues = nodeValues + [G.nodes[i][colorAtt]]
		# convert node attribute values into colors:
		nodeColors = cm.plasma(plt.Normalize(min(nodeValues),max(nodeValues))(nodeValues))
		# convert rgb into hex:
		for i in range(n_nodes):
			print(co.rgb2hex(nodeColors[i,0:3]))
		print(nodeColors)

	# get hex color for matplotlib 'grey'
	greyHex = co.to_hex('grey')

	for i in range(n_nodes):
		A.get_node(i).attr['style'] = 'filled,setlinewidth(0)'
		if colorAtt is not None:
			A.get_node(i).attr['fillcolor']=co.rgb2hex(nodeColors[i,0:3])
		else:
			A.get_node(i).attr['fillcolor']="#C62E3A"

		A.get_node(i).attr['label'] = ''

	A.edge_attr['linecolor']=greyHex	
	A.node_attr['shape']='circle'
	A.layout() # default to neato
	A.layout(prog='circo') # use circo

	A.draw(fname)


def _plotPointsAndHist(data, D, axPoints, axHist, labels=None):
	distances = []
	for i in range(len(D[0,:])):
		for j in range(i):
			distances = distances + [D[i,j]]
	_plotPointCloud(data, axPoints, labels=labels)
	axHist.hist(distances)


def _plotPointCloud(data, ax, labels=None):

	ax.scatter(
		data[:,0],
		data[:,1],
		c=labels,
		cmap='plasma')

	ax.set_xlim(0,1)
	ax.set_ylim(0,1)
	ax.set_xticks([], [])
	ax.set_yticks([], [])

