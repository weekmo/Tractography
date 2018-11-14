
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
from dipy.tracking.streamline import transform_streamlines, set_number_of_points
from dipy.align.streamlinear import compose_matrix44

from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles, clusters_colors, draw_clusters
from src.tractography.Utils import pca_transform_norm, normalize, kd_tree_cost, dist_new, costs

shape = (20,7)
affines = []
mat = np.array([20,20,20,180,180,120,1])
for i in range(shape[0]):
    mat[:-1] = mat[:-1]/1.23
    affines.append(compose_matrix44(mat))
    
#static = read_ply('data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

#con_static = np.concatenate(static)
#con_moving = np.concatenate(moving)

sep_moving = set_number_of_points(moving,shape[0])

new_moving = []
for i,j in zip(sep_moving,moving):
    kdtree = KDTree(j)
    # Set used to avoid repeatition if the # of poits less than the sat #
    new_moving.append(j[list(set(np.hstack(kdtree.query(i,k=1)[1])))])

print(moving[0][[1,2,3,1]])



for i in range(lenght):
    affines.append(compose_matrix44((((lenght-i)/lenght)*l1) + ((i/lenght)*l2)))

new_con_moving = np.array([apply_affine(mat,s) for mat,s in zip(affines,moving[0])])

draw_bundles([new_moving])
'''
options = {'maxcor': 10, 'ftol': 1e-7,'gtol': 1e-5, 'eps': 1e-8,'maxiter': 100000}

shape = (len(con_moving),len(x0[0]))
m = Optimizer(dist_new, x0,args=(con_static,con_moving,shape,.3,500),method='L-BFGS-B',options=options)
m.print_summary()
'''
