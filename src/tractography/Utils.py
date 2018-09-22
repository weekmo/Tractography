import numpy as np
from dipy.segment.quickbundles import bundles_distances_mdf
from dipy.segment.metric import mdf
from src.tractography.io import read_ply
from src.tractography.viz import draw_brain
from src.tractography.registration import register
from dipy.tracking.streamline import (unlist_streamlines,
                                      center_streamlines,
                                      set_number_of_points,
                                      transform_streamlines)
from dipy.align.streamlinear import compose_matrix44, bundle_min_distance_fast
from dipy.core.optimize import Optimizer
from dipy.core.geometry import compose_transformations
from sklearn.neighbors import KDTree
from scipy.ndimage.interpolation import affine_transform
from sklearn.decomposition import PCA  # ,IncrementalPCA


def distance_euc(x0, static, moving):
    aff = compose_matrix44(x0)
    moving = transform_streamlines(moving, aff)
    dist_mat = bundles_distances_mdf(static, moving)
    idx = np.argmin(dist_mat, axis=1)
    static = np.array(static)
    moving = np.array(moving)[idx]
    cost = np.sum(np.linalg.norm(static - moving, axis=2))
    # cost = np.average(np.linalg.norm(static-moving,axis=2))
    return cost


def distance_mdf(x0, static, moving):
    # Minimum Direct Flip (MDF) distance
    aff = compose_matrix44(x0)
    moving = transform_streamlines(moving, aff)
    dist_mat = bundles_distances_mdf(static, moving)
    # idx = np.argmin(dist_mat, axis=1)
    vals = np.min(dist_mat, axis=1)
    cost = np.sum(vals)
    return cost


def distance_kdtree(x0, static, moving):
    # joint bundles
    affine = compose_matrix44(x0)
    moving = transform_streamlines(moving, affine)
    tree = KDTree(moving)
    cost = np.sum(tree.query(static, k=1)[0])
    return cost


"""
def pca_transform(static,moving):
    # joint bundles
    # IncrementalPCA(batch_size=10)
    pca = PCA(n_components=3)
    return pca.fit_transform(static),pca.fit_transform(moving)
"""
