import numpy as np
import sys
from src.tractography.io import read_ply
from src.tractography.Utils import pca_transform, distance_kdTree9D,make9D
from src.tractography.viz import draw_brain
from src.tractography.registration import registration_icp,register
from sklearn.neighbors import KDTree
from dipy.tracking.streamline import set_number_of_points,transform_streamlines
from dipy.align.streamlinear import compose_matrix44
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances

# TODO clustering

static = read_ply('../data/197348/m_ex_atr-left_shore.ply')
moving = read_ply('../data/164939/m_ex_atr-left_shore.ply')

con_target = np.concatenate(static)
con_subject = np.concatenate(moving)

kmeans = KMeans(3).fit(con_subject)
print(kmeans.cluster_centers_ )
print(euclidean_distances(kmeans.cluster_centers_))