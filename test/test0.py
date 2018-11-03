import numpy as np
# x = [["a","b"], ["c"]]
# print([j for i in x for j in i])
from src.tractography.io import read_ply
# from src.tractography.viz import clusters_colors,draw_clusters, draw_bundles
from pyclustering.cluster.kmedoids import kmedoids

static = read_ply('../data/132118/m_ex_atr-left_shore.ply')

# km = kmedoids(np.concatenate(static),[0,1,2])
km = kmedoids(static, [0, 1, 2])
km.process()
# print(km.get_clusters())
