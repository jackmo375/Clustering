import matplotlib.pyplot as plt
import networkx as nx

from graphviz import Graph
import pygraphviz as pgv

from matplotlib import rcParams
rcParams['axes.linewidth'] = 2.5 # set the value globally
rcParams['axes.edgecolor'] = 'grey'
rcParams["figure.figsize"] = [10,10]
rcParams['xtick.labelsize'] = 15
rcParams['ytick.labelsize'] = 15
rcParams['xtick.color'] = 'grey'
rcParams['ytick.color'] = 'grey'
rcParams['lines.linewidth'] = 2.5


def plotData(data, labels=None, fName=None, annotate=True):
	'''
	Plots data set on fixed [0,1]^2 grid
	'''
	plt.scatter(data[:,0], data[:,1], c=labels)

	if annotate==True:
		for i in range(len(data)):
			plt.annotate(f" {i}", (data[i,0], data[i,1])) 

	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.xticks([], [])
	plt.yticks([], [])

	# save figure:
	if fName != None:
		plt.savefig(fName)

	#plt.show()

def plotGraph(G):
	'''
	Plots a networkX graph, G
	'''
	A = nx.nx_agraph.to_agraph(G)
	dataDir = '../data/'
	label = 'simple'
	nx.nx_agraph.write_dot(G, dataDir+label+'.gv')

	#print(A)

	nx.draw(G, 
		node_color='C3',	# red
		edge_color='C7')	# grey
	plt.savefig('../media/completeGraph.pdf')
	plt.show()

def plotGraphs(graphSet):
	'''
	Plots a set of graphs on the same plot
	'''
	for graph in graphSet:
		nx.draw(graph)
	plt.show()

def plotPointsGraph(data):
	nPoints = len(data[:,0])
	G = nx.Graph()
	G.add_nodes_from(range(nPoints))

	A = nx.nx_agraph.to_agraph(G)
	A.node_attr['shape']='circle'
	A.layout() # default to neato
	A.layout(prog='circo') # use circo

	dataDir = '../data/'
	label = 'points'
	A.draw(dataDir+label+'.gv')


def plotClustersGraph(labels, fname):
	'''
	Plots a set of clusters in graph form
		+ clusterLabels is output from 
			Agglomerative clutering object
	'''

	# get number of clusters:
	nClusters = max(labels) + 1
	nPoints   = len(labels)

	# construct graph:
	G = nx.Graph()
	# add points:
	G.add_nodes_from(range(nPoints))
	# add clusters: 
	G.add_nodes_from(range(nClusters)) 
		# cluster ids are nPoints,...,Npoints + nClusters - 1

	# re-index the points according to their clusters:
	subGraphNodes = []
	for i in range(nClusters):
		subGraphNodes = subGraphNodes + [[]]
	for i in range(nPoints):
		j = labels[i]
		subGraphNodes[j] = subGraphNodes[j] + [i]
	# join the points to their cluster nodes:
	for i in range(nClusters):
		for node in subGraphNodes[i]:
			G.add_edge(nPoints+i, node)

	# print it:
	A = nx.nx_agraph.to_agraph(G)
	for i in range(nPoints,nPoints+nClusters):
		A.get_node(i).attr['style'] = 'filled'
		A.get_node(i).attr['fillcolor']="#C62E3A"
		A.get_node(i).attr['label'] = ''

	A.node_attr['shape']='circle'
	A.layout() # default to neato
	A.layout(prog='circo') # use circo

	A.draw(fname)

def plotElbowTest(data, K, unExVars, fname=None):

	plt.figure(figsize=(10,5))

	plt.subplot(1, 2, 1)
	plt.scatter(data[:,0], data[:,1])

	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.xticks([], [])
	plt.yticks([], [])

	plt.subplot(1, 2, 2)
	plt.plot(K, unExVars)
	plt.plot(K, unExVars, 'ro')
	plt.xticks(K)
	plt.yticks([])

	if fname!=None:
		plt.savefig(fname)

	plt.show()