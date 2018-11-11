
# x = [["a","b"], ["c"]]
# print([j for i in x for j in i])
import numpy as np
import sys
from random import random
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree
from sklearn.metrics.pairwise import paired_euclidean_distances

from scipy.sparse.linalg import lsqr
from scipy.sparse.linalg import LinearOperator
#from scipy.sparse import csc_matrix

from nibabel.affines import apply_affine
from dipy.core.optimize import Optimizer
from dipy.tracking.streamline import transform_streamlines
from dipy.align.streamlinear import compose_matrix44

from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles, clusters_colors, draw_clusters
from src.tractography.Utils import pca_transform_norm, normalize, kd_tree_cost, dist_new, costs


static = read_ply('data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

con_static = np.concatenate(static)
con_moving = np.concatenate(moving)

x0 = np.array([[0,0,0, 0,0,0, 1] for __ in con_moving])

options = {'maxcor': 10, 'ftol': 1e-7,
               'gtol': 1e-5, 'eps': 1e-8,
               'maxiter': 100000}
shape = (len(con_moving),7)
m = Optimizer(dist_new, x0,args=(con_static,con_moving,shape,.3,500),method='L-BFGS-B',options=options)
m.print_summary()

affines = np.reshape(x0,shape)
new_moving = np.array([apply_affine(compose_matrix44(mat),vertex) for mat,vertex in zip(affines,con_moving)])

dist_cost = kd_tree_cost(con_moving,new_moving,500)
print("Dist Cost: ",dist_cost)

kdtree = KDTree(con_moving)
idx = kdtree.query_radius(con_moving,.3)

stiff_cost = np.sum([np.sum([np.linalg.norm(new_moving[i] - j) for j in new_moving[idx[i]]]) for i in range(len(new_moving))])
print("stiff",stiff_cost)
dist_new(x0,con_moving,con_moving,shape,.3,500)