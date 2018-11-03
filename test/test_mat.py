import time
import sys
import random
import numpy as np

from src.tractography.io import read_ply
from src.tractography.Utils import distance_kdTree9D, make9D, Clustering, distance_kdtree, \
    pca_transform_norm, normalize
from src.tractography.viz import draw_bundles
from src.tractography.registration import registration_icp
from sklearn.neighbors import KDTree
from dipy.tracking.streamline import set_number_of_points, transform_streamlines
from dipy.align.streamlinear import compose_matrix44
from dipy.core.optimize import Optimizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances

# ToDo: Pictures for registration:
"""
    1- With kmeans clustering and without
    2- With PCA and without
    3- Use different distance functions (MDF, 9D, Points Cloud)
"""
"""
size 03, translation.
size 06, translation + rotation.
size 07, translation + rotation + isotropic scaling.
size 09, translation + rotation + anisotropic scaling.
size 12, translation + rotation + scaling + shearing.
"""
static = read_ply('data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')
start = time.time()
medoids = registration_icp(static, moving,pca=False)
print("Time for kmedoids", time.time() - start)
start = time.time()
mean = registration_icp(static, moving)
print("Time for kmeans", time.time() - start)

start = time.time()
no_cluster = registration_icp(static, moving)
print("Time for No Clustering", time.time() - start)

draw_bundles([static, moving, medoids, mean, no_cluster], [[1, 0, 0], [0, 0, 1], [0, 1, 0], [1, 1, 0], [0, 0, 1]])
draw_bundles([static,mean],[[1,0,0],[0,0,1]])