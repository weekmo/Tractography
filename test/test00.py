
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
from src.tractography.Utils import pca_transform_norm, normalize, kd_tree_cost, dist_new, costs, transform

static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('../data/150019/m_ex_atr-right_shore.ply')

#con_static = np.concatenate(static)
#con_moving = np.concatenate(moving)

length = 5
x0 = np.array([[0,0,0, 0,0,0, 1] for _ in range(length)])

options = {'maxcor': 10, 'ftol': 1e-7,'gtol': 1e-5, 'eps': 1e-8,'maxiter': 100000}

m = Optimizer(dist_new, x0,args=(static,moving,length,.3,500,1),method='L-BFGS-B',options=options)
m.print_summary()
x = m.xopt.reshape((5,7))
new_moving = transform(x,moving)
draw_bundles([static,new_moving],[[1,0,0],[0,0,1]])