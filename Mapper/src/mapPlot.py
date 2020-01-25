import matplotlib.pyplot as plt

def plotShapeHist(data, D, labels=None):

	n_points = len(D[:,0])
	if labels is None:
		labels = [0]*n_points
	n_clusters = max(labels)+1

	# generate n_clusters x 2 subplots:
	fig, axes = plt.subplots(
		2, 
		1+n_clusters, 
		figsize=(5*(1+n_clusters),10))

	if n_clusters == 1:
		_plotPointsAndHist(data, D, axes[0], axes[1])
	else:
		_plotPointsAndHist(data, D, axes[0,0], axes[1,0])
		for i in range(n_clusters):
			_plotPointsAndHist(data, D, axes[0,i+1], axes[1,i+1])

	plt.show()

def subsetData(data, labels):
	pass

def subsetDist(D, labels):
	pass

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
		c=labels)

	ax.set_xlim(0,1)
	ax.set_ylim(0,1)
	ax.set_xticks([], [])
	ax.set_yticks([], [])


