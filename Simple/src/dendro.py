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
    #data_mat = sgt.genPoisson(N)   # uniform point cloud

    # convert data to network:
    dist_mat = snt.getDistanceMatrix(data_mat)

    # perform the clustering:
    ## setting distance_threshold=0 ensures we compute the full tree.
    model = AgglomerativeClustering(
        linkage='average',
        affinity='precomputed',
        distance_threshold=0, 
        n_clusters=None).fit(dist_mat)

    # plot the top three levels of the dendrogram
    spt.plot_dendrogram(
        data_mat,
        model, 
        truncate_mode='level', 
        p=10, 
        fname='../media/dendro1.png')


if __name__ == '__main__':
    main()