import numpy as np
from dipy.segment.quickbundles import bundles_distances_mdf
from dipy.tracking.streamline import transform_streamlines
from dipy.align.streamlinear import compose_matrix44
from sklearn.neighbors import KDTree
from sklearn.decomposition import PCA


def distance_euc(x0, static, moving):
    aff = compose_matrix44(x0)
    moving = transform_streamlines(moving, aff)
    dist_mat = bundles_distances_mdf(static, moving)
    idx = np.argmin(dist_mat, axis=1)
    static = np.array(static)
    moving = np.array(moving)[idx]
    cost = np.sum(np.linalg.norm(static - moving, axis=2))
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
    tree = KDTree(np.concatenate(moving))
    cost = np.sum(tree.query(np.concatenate(static), k=1)[0])
    return cost


def pca_transform(static,moving):
    con_target = np.concatenate(static)
    con_subject = np.concatenate(moving)

    pca = PCA(n_components=3)

    pca = pca.fit(con_subject)
    prev = pca.components_.T

    pca = pca.fit(con_target)

    aff = np.dot(prev,pca.components_)

    mean_s = np.mean(con_subject,axis=0)
    mean_t = np.mean(con_target,axis=0)
    return [np.dot((i-mean_s),aff)+mean_t for i in moving]

