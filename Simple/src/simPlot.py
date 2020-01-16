import matplotlib.pyplot as plt

from matplotlib import rcParams
rcParams['axes.linewidth'] = 2.5 # set the value globally
rcParams['axes.edgecolor'] = 'grey'
rcParams["figure.figsize"] = [10,10]

def plotData(data, labels=None, fName=None):
	'''
	Plots data set on fixed [0,1]^2 grid
	'''
	plt.scatter(data[:,0], data[:,1], c=labels)
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.xticks([], [])
	plt.yticks([], [])

	# save figure:
	if fName != None:
		plt.savefig(fName)

	plt.show()