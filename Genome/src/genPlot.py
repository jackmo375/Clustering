# import local modules:
from genGenerate import NUCL_VEC

# import enviroment modules:
import matplotlib.pyplot as plt 
from scipy.cluster import hierarchy
import networkx as nx

import matplotlib.ticker as mtick
from matplotlib import rcParams
rcParams['axes.linewidth'] = 2.5 # set the value globally
rcParams['axes.edgecolor'] = 'grey'
rcParams["figure.figsize"] = [10,10]
rcParams['xtick.labelsize'] = 15
rcParams['ytick.labelsize'] = 15
rcParams['xtick.color'] = 'grey'
rcParams['ytick.color'] = 'grey'
rcParams['lines.linewidth'] = 2.5
rcParams['axes.labelsize'] = 'xx-large'
rcParams['axes.labelcolor'] = 'grey'

def plotRawPanGenome(panGenome, fname=None, show=True):

	fig, ax = plt.subplots()

	createDataPlot(panGenome, fig, ax)

	n_genomes = len(panGenome[:,0])

	ax.set_yticks(range(n_genomes))
	ax.set_xlabel('nucleotides')
	ax.set_ylabel('genomes')
	plt.tight_layout()

	if fname is not None:
		plt.savefig(fname)

	if show is True:
		plt.show()

def createDataPlot(panGenome, fig, ax):

	n_p = len(panGenome[:,0])
	n_g = len(panGenome[0,:])

	im = ax.imshow(panGenome, cmap="Dark2")

	for i in range(n_p):
		for j in range(n_g):
			text = ax.text(j, i, NUCL_VEC[panGenome[i, j]],
				ha="center", va="center", color="w")

	ax.set_xticks([])
	ax.set_yticks([])

	fig.tight_layout()

def plotJumpTest(data, jump_obj, fname=None):

	fig, axes = plt.subplots(2, 3, figsize=(15, 10))
	hierarchy.set_link_color_palette(['C1', 'C2', 'C3', 'C4'])
	kvec = range(1,jump_obj.maxclusters+1)

	# plot raw data:
	createDataPlot(data, fig, axes[0,0])
	axes[0,0].set_yticks([])


	axes[0,1].plot(kvec,jump_obj.w_log_vec)
	axes[0,1].plot(kvec,jump_obj.w_log_vec, 'ro')
	axes[0,1].set_xticks(kvec)
	axes[0,1].set_yticks([])


	hierarchy.dendrogram(
		jump_obj.linkage_mat, 
        truncate_mode='none', 
        #p=jump_obj.maxclusters,
		above_threshold_color='C0',
		ax=axes[0,2])
	axes[0,2].set_xticks([])


	axes[1,0].plot(kvec,jump_obj.w_log_vec)
	axes[1,0].plot(kvec,jump_obj.w_log_vec, 'ro')
	axes[1,0].plot(kvec,jump_obj.wnull_log_average_vec)
	axes[1,0].plot(kvec,jump_obj.wnull_log_average_vec, 'ro')
	axes[1,0].set_xticks(kvec)
	axes[1,0].set_yticks([])


	axes[1,1].plot(kvec,jump_obj.gap)
	axes[1,1].plot(kvec,jump_obj.gap, 'ro')
	axes[1,1].set_xticks(kvec)
	axes[1,1].set_yticks([])


	hierarchy.dendrogram(
		jump_obj.null_linkage_mat, 
        truncate_mode='none', 
        #p=jump_obj.maxclusters,
		above_threshold_color='C0',
		ax=axes[1,2])
	axes[1,2].set_xticks([])


	if fname is not None:
		plt.savefig(fname)

	plt.show()

def plotClustersGraph(labels, fname=None):
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