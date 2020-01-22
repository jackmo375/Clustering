# Authors: Mathew Kallada, Andreas Mueller
# License: BSD 3 clause
"""
=========================================
Plot Hierarchical Clustering Dendrogram
=========================================
This example plots the corresponding dendrogram of a hierarchical clustering
using AgglomerativeClustering and the dendrogram method available in scipy.
"""

# import enviroment modules:
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# import local modules:
import simGenerate as sgt
import simPlot as spt
import simNetwork as snt
import simStats as sst

def main():

    # set program constants:
    K = 10  # max number of clusters
    B = 100 # number of null realisations created by gap test
    N = 100 # number of points in the input data cloud

    # generate clusters:
    n1, n2, n3 = 20, 20, 10
    n4 = N - n1 - n2 - n3
    cluster_vec = [
        sgt.genCluster((0.3,0.7), 0.1, n1),
        sgt.genCluster((0.1,0.3), 0.1, n2),
        sgt.genCluster((0.7,0.5), 0.1, n3),
        sgt.genCluster((0.5,0.1), 0.1, n4)
    ]

    # create data set:
    data_mat = np.concatenate(
        (cluster_vec[0],cluster_vec[1],cluster_vec[2],cluster_vec[3]), 
        axis=0)
    data_mat = sgt.genPoisson(N)   # uniform point cloud

    # convert data to network:
    dist_mat = snt.getDistanceMatrix(data_mat)

    den_obj = sst.DendroTest(K).fit(dist_mat)

    # plot the top p levels of the dendrogram
    spt.plotDendroTest(
        data_mat,
        den_obj, 
        fname='../media/dendro3.png')


if __name__ == '__main__':
    main()