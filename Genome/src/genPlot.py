# import local modules:
from genGenerate import NUCL_VEC

# import enviroment modules:
import matplotlib.pyplot as plt 
from scipy.cluster import hierarchy

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

def plotRawPanGenome(panGenome, fname=None):

	fig, ax = plt.subplots()

	createDataPlot(panGenome, fig, ax)

	ax.set_xlabel('nucleotides')
	ax.set_ylabel('genomes')

	if fname is not None:
		plt.savefig(fname)

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
	axes[1,0].set_yticks([])


	axes[1,1].plot(kvec,jump_obj.gap)
	axes[1,1].plot(kvec,jump_obj.gap, 'ro')
	axes[1,1].set_xticks(kvec)
	axes[1,1].set_yticks([])


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