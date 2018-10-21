import numpy as np
import sys
from src.tractography.io import read_ply
from src.tractography.Utils import pca_transform, distance_kdTree9D, make9D,Clustering
from src.tractography.viz import draw_brain
from src.tractography.registration import registration_icp, register
from sklearn.neighbors import KDTree
from dipy.tracking.streamline import set_number_of_points, transform_streamlines
from dipy.align.streamlinear import compose_matrix44
from dipy.core.optimize import Optimizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances


static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('../data/164939/m_ex_atr-left_shore.ply')

new_moving = registration_icp(static,moving,affine=[0,0,0, 0,0,0, 0,0,0, 0,0,0])

draw_brain([static,moving,new_moving],[[1,0,0],[0,0,1],[0,1,0]])