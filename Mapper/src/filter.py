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
	c = (0.5, 0.5)	# center of cluster

	# generate the data:
	#data = mgt.genCigar(0.3,0.05,c,N, rot_angle=0.3*np.pi)
	#data = mgt.genDisk(0.3, c, N)
	#data = mgt.genAnnulus(0.1, 0.3, c, N)
	#data = mgt.genRect(0.2,0.5,c,N)
	#data = mgt.genCross(0.8,0.6,0.1,c,N,rot_angle=7.)
	data = mgt.genS(0.6, 0.1,c,N)
	#data = mgt.genEight(0.6, 0.1,c,N)
	#data = mgt.genGauss(c, 0.1, 0.02, N, rot_angle=10.)

	# pairwise separation matrix:
	dist = snt.getDistanceMatrix(data)

	# compute filter values
	fil_vec = mst.filterDensity(dist, 0.1)
	#fil_vec = mst.filterEccentric(dist, 3)
	#fil_vec = mst.filterLinfinity(dist)

	# print stats:
	st_obj = mst.StatsTable(dist)
	st_obj.printStatsTable()

	# plot the data:
	#mpt.plotPoints(data, labels=fil_vec, fname='../media/cigar.ecc.png')
	#mpt.plotShapeHist(data,dist,fname='../media/cigar.shapeHist.png')
	mpt.plotPointsFilterHist(data,fil_vec, fname='../media/s.filterHist.den.png')


if __name__ == '__main__':
	main()