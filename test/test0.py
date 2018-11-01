import numpy as np
#x = [["a","b"], ["c"]]
#print([j for i in x for j in i])
from src.tractography.io import read_ply
from sklearn.cluster import KMeans
from src.tractography.viz import clusters_colors,draw_clusters
#from pyclustering.cluster.kmedoids import kmedoids

static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
#moving = read_ply('../data/150019/m_ex_atr-right_shore.ply')

colours = [[1,0,0],[0,1,0],[0,0,1],[1,1,0]]

kmean = KMeans(4).fit(np.concatenate(static))
static_clusters = clusters_colors(static,colours,kmean.labels_)

draw_clusters([static_clusters])

"""
kmean = KMeans(4).fit(np.concatenate(moving))
moving_clusters = clusters_colors(moving,colours,kmean.labels_)

draw_clusters([static_clusters,moving_clusters])

kmed = kmedoids(static[0], [0,1,2])
kmed.process()
kmed.get_clusters()
"""