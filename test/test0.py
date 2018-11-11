
# x = [["a","b"], ["c"]]
# print([j for i in x for j in i])
import numpy as np
from random import random
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree
from sklearn.metrics.pairwise import paired_euclidean_distances

#from scipy.sparse.linalg import lsqr
#from scipy.sparse import csc_matrix

from dipy.tracking.streamline import transform_streamlines
from dipy.align.streamlinear import compose_matrix44

from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles, clusters_colors, draw_clusters
from src.tractography.Utils import pca_transform_norm, normalize

k = 20
static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('../data/150019/m_ex_atr-right_shore.ply')

con_static = np.concatenate(static)
con_moving = np.concatenate(moving)

# Clustering
kmeans = KMeans(k).fit(con_moving)
colours = [[random(), random(), random()] for _ in range(k)]
new_moving = clusters_colors(moving,colours,kmeans.labels_)
draw_clusters(new_moving)

# KDTree
kdtree = KDTree(con_moving)
idx = kdtree.query_radius(con_moving,.3)

cost=0
for i in range(len(con_moving)):
    x = con_moving[i]
    cost += np.sum([np.linalg.norm(x - i) for i in con_moving[idx[i]]])
print(cost)