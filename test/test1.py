import time
import sys
import random
import numpy as np
from sklearn.neighbors import KDTree
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from src.tractography.io import read_ply
from src.tractography.viz import draw_brain
from src.tractography.Utils import Clustering, pca_transform_norm
from src.tractography.registration import registration_icp
from scipy.optimize import minimize

static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('../data/150019/m_ex_atr-right_shore.ply')

new_moving = pca_transform_norm(static, moving)

draw_brain([static, moving, new_moving], [[1, 0, 0], [0, 0, 1], [0, 1, 0]])
