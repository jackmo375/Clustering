import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.cluster import hierarchy

from graphviz import Graph
import pygraphviz as pgv

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

def plotData(
	data, 
	labels=None, 
	fname=None, 
	annotate=False, 
	show=True,
	pointSize=None):
	'''
	Plots data set on fixed [0,1]^2 grid
	'''
	if labels is None:
		plt.scatter(
			data[:,0], 
			data[:,1], 
			edgecolors='r', 
			s=pointSize,
			facecolors='none')
	else:
		plt.scatter(
			data[:,0],
			data[:,1],
			c=labels)

	if annotate==True:
		for i in range(len(data)):
			plt.annotate(
				f"{i}", 
				(data[i,0]+0.02, data[i,1]+0.02),
				 color='grey',
				 weight='bold',
				 size=15) 

	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.xticks([], [])
	plt.yticks([], [])

	# save figure:
	if fname is not None:
		plt.savefig(fname)

	if show is True:
		plt.show()

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


def plotElbowTest(data, elbow_obj, fname=None):

	plt.figure(figsize=(10,5))

	k_vec = range(1,elbow_obj.maxclusters+1)

	plt.subplot(1, 2, 1)
	plt.scatter(data[:,0], data[:,1])
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.xticks([], [])
	plt.yticks([], [])

	plt.subplot(1, 2, 2)
	plt.plot(k_vec, elbow_obj.w_vec)
	plt.plot(k_vec, elbow_obj.w_vec, 'ro')
	plt.xticks(k_vec)
	plt.yticks([])

	if fname!=None:
		plt.savefig(fname)

	plt.show()


def plotGapTest(data, gap_obj, fname=None):

	plt.figure(figsize=(10,10))

	k_vec = range(1,gap_obj.maxclusters+1)

	# plot points:
	plt.subplot(2, 2, 1)
	plt.scatter(data[:,0], data[:,1])
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.xticks([], [])
	plt.yticks([], [])

	# plot elbow:
	plt.subplot(2, 2, 2)
	plt.plot(k_vec, gap_obj.w_log_vec)
	plt.plot(k_vec, gap_obj.w_log_vec, 'ro')
	plt.xticks(k_vec)
	plt.yticks([])

	# plot comparison:
	plt.subplot(2, 2, 3)
	plt.plot(k_vec, gap_obj.w_log_vec)
	plt.plot(k_vec, gap_obj.w_log_vec, 'ro')
	plt.plot(k_vec, gap_obj.wnull_log_average_vec)
	plt.plot(k_vec, gap_obj.wnull_log_average_vec, 'ro')
	plt.xticks(k_vec)
	plt.yticks([])

	# plot gap curve:
	plt.subplot(2, 2, 4)
	plt.plot(k_vec, gap_obj.gap)
	plt.plot(k_vec, gap_obj.gap, 'ro')
	plt.xticks(k_vec)
	plt.yticks([])

	if fname is not None:
		plt.savefig(fname)

	plt.show()

def plotDendroTest(data, den_obj, fname=None):

	fig, axes = plt.subplots(1, 3, figsize=(15, 5))

	# plot points:
	axes[0].scatter(data[:,0], data[:,1])
	axes[0].set_xlim(0,1)
	axes[0].set_ylim(0,1)
	axes[0].set_xticks([], [])
	axes[0].set_yticks([], [])

	# Plot the corresponding dendrogram
	hierarchy.set_link_color_palette(['C1', 'C2', 'C3', 'C4'])
	hierarchy.dendrogram(
		den_obj.linkage_mat, 
        truncate_mode='level', 
        p=den_obj.maxclusters,
		above_threshold_color='C0',
		ax=axes[1])
	axes[1].set_xticks([])

	p    = den_obj.maxclusters+1
	kvec = range(1,p)
	distances = den_obj.linkage_mat[:,2]
	axes[2].plot(kvec,distances[:-p:-1])
	axes[2].plot(kvec,distances[:-p:-1], 'ro')
	axes[2].set_xticks(kvec)


	if fname is not None:
		plt.savefig(fname)

	plt.show()


def plotJumpTest(data, jump_obj, fname=None):

	fig, axes = plt.subplots(2, 3, figsize=(15, 10))
	hierarchy.set_link_color_palette(['C1', 'C2', 'C3', 'C4'])

	# plot points:
	axes[0,0].scatter(data[:,0], data[:,1])
	axes[0,0].set_xlim(0,1)
	axes[0,0].set_ylim(0,1)
	axes[0,0].set_xticks([], [])
	axes[0,0].set_yticks([], [])

	kvec = range(1,jump_obj.maxclusters+1)
	axes[0,1].plot(kvec,jump_obj.w_log_vec)
	axes[0,1].plot(kvec,jump_obj.w_log_vec, 'ro')
	axes[0,1].set_xticks(kvec)

	hierarchy.dendrogram(
		jump_obj.linkage_mat, 
        truncate_mode='level', 
        p=jump_obj.maxclusters,
		above_threshold_color='C0',
		ax=axes[0,2])
	axes[0,2].set_xticks([])

	axes[1,0].plot(kvec,jump_obj.w_log_vec)
	axes[1,0].plot(kvec,jump_obj.w_log_vec, 'ro')
	axes[1,0].plot(kvec,jump_obj.wnull_log_average_vec)
	axes[1,0].plot(kvec,jump_obj.wnull_log_average_vec, 'ro')
	axes[1,0].set_xticks(kvec)

	axes[1,1].plot(kvec,jump_obj.gap)
	axes[1,1].plot(kvec,jump_obj.gap, 'ro')
	axes[1,1].set_xticks(kvec)

	hierarchy.dendrogram(
		jump_obj.null_linkage_mat, 
        truncate_mode='level', 
        p=jump_obj.maxclusters,
		above_threshold_color='C0',
		ax=axes[1,2])
	axes[1,2].set_xticks([])

	if fname is not None:
		plt.savefig(fname)

	plt.show()


def plotClustersAndGraph(data, labels, ffolder, flabel):


	plotData(
		data,
		annotate=True,
		fname=ffolder+flabel+'1.png',
		show=False,
		pointSize=400)

	plotClustersGraph(labels, fname=ffolder+flabel+'2.png')