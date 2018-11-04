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

# ToDo: Use different distance functions with and without clustering
"""
The word anisotropy comes the Greek words anisos (unequal) + tropos (turn).
An entity such as a wavelet is anisotropic, provided it has a different magnitude or properties when measured in different directions.
In science, an anisotropic entity has properties that differ according to the direction of measurement.

size 03, translation.
size 06, translation + rotation.
size 07, translation + rotation + isotropic scaling.
size 09, translation + rotation + anisotropic scaling.
size 12, translation + rotation + scaling + shearing.
"""
static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('../data/150019/m_ex_atr-right_shore.ply')

moving1 = registration_icp(static, moving, clustering='kmedoids',dist='tract',pca=False)
moving2 = registration_icp(static, moving, clustering='kmeans',dist='tract',pca=False)
moving3 = registration_icp(static, moving, dist='tract',pca=False)

draw_bundles([static,moving3],[[1,0,0],[0,0,1]])