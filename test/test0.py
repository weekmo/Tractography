
# x = [["a","b"], ["c"]]
# print([j for i in x for j in i])
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree

from dipy.tracking.streamline import transform_streamlines
from dipy.align.streamlinear import compose_matrix44

from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles, clusters_colors, draw_clusters
from src.tractography.Utils import pca_transform_norm, normalize
max_dist = 50
k=3
beta = 999
x0 = [0,0,0]

moving = read_ply('data/132118/m_ex_atr-left_shore.ply')
#static = read_ply('data/132118/m_ex_atr-right_shore.ply')
static = read_ply('data/150019/m_ex_atr-right_shore.ply')
moving1 = pca_transform_norm(static,moving,500)
con_static = np.concatenate(static)
con_moving = np.concatenate(moving)

kmeans = KMeans(k).fit(con_moving)
cluster1 = clusters_colors(moving,[[1,0,0],[1,1,0],[0,0,1]],kmeans.labels_)
draw_clusters(cluster1)
idx = {i: np.where(kmeans.labels_ == i)[0] for i in range(k)}

draw_bundles([static,moving1],[[1,0,0],[0,0,1]])
