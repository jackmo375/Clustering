# Modules
## enviroment:
import numpy as np

## local:
import mapGenerate as mgt
import mapPlot as mpt
import simNetwork as snt
import mapStats as mst

def main():

	N = 200		# number of points in each cluster
	M = 3		# number of sets in the cover
	K = 5  		# max number of clusters in each cover member set
	B = 100 	# number of null realisations created each gap test
	c = (0.5, 0.5)	# center of cluster

	# generate the data:
	#data = mgt.genCigar(0.3,0.05,c,N, rot_angle=0.3*np.pi)
	#data = mgt.genDisk(0.3, c, N)
	#data = mgt.genAnnulus(0.1, 0.3, c, N)
	#data = mgt.genRect(0.2,0.5,c,N)
	#data = mgt.genCross(0.8,0.6,0.1,c,N,rot_angle=0.)
	#data = mgt.genS(0.6, 0.1,c,N)
	#data = mgt.genEight(0.6, 0.1,c,N)
	data = mgt.genGauss(c, 0.1, 0.02, N, rot_angle=10.)

	# pairwise separation matrix:
	dist = snt.getDistanceMatrix(data)

	# print stats:
	st_obj = mst.StatsTable(dist)
	st_obj.printStatsTable()

	# compute filter values
	#fil_vec = mst.filterDensity(dist, 0.1)
	#fil_vec = mst.filterEccentric(dist, 3)
	fil_vec = mst.filterLinfinity(dist)

	eps = 0.4

	# initialise mapper object:
	mp = mst.Mapper(
		min(fil_vec),
		max(fil_vec),
		M,
		eps,
		K, B)
	mp.fit(data, dist, fil_vec)

	# plot the data:
	#mpt.plotPoints(data, labels=fil_vec, fname='../media/cigar.ecc.png')
	#mpt.plotShapeHist(data,dist,fname='../media/cigar.shapeHist.png')
	mpt.plotPointsFilterHist(data,fil_vec, fname='../media/cross.filterHist.den.png')
	mpt.plotGraph(mp.clusterGraph, '../media/gaus.mapperGraph.png', colorAtt='avfvalue')


if __name__ == '__main__':
	main()