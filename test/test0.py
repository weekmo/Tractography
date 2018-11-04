
# x = [["a","b"], ["c"]]
# print([j for i in x for j in i])
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree

from dipy.tracking.streamline import transform_streamlines
from dipy.align.streamlinear import compose_matrix44

from src.tractography.io import read_ply

max_dist = 50
k=3
beta = 999
x0 = [0,0,0]

moving = read_ply('../data/132118/m_ex_atr-left_shore.ply')
static = read_ply('../data/150019/m_ex_atr-right_shore.ply')

affine = compose_matrix44
affine = affine(x0)
moving = transform_streamlines([con_moving], affine)
print(moving)
con_static = np.concatenate(static)
con_moving = np.concatenate(moving)

tree = KDTree(con_moving)
dist_list = np.hstack(tree.query(con_static, k=1)[0])
cost = np.sum(dist_list[np.where(dist_list < max_dist)])

kmeans = KMeans(k).fit(con_moving)
print(kmeans.cluster_centers_)
idx = {i: np.where(kmeans.labels_ == i)[0] for i in range(k)}

clustering_cost = 0
for i in range(k):
    clustering_cost += np.linalg.norm(
    kmeans.cluster_centers_[i] - np.mean(con_moving[idx[i]], axis=0))
print(cost + beta * clustering_cost)