import numpy as np
import sys
from dipy.segment.quickbundles import bundles_distances_mdf
from dipy.tracking.streamline import transform_streamlines,set_number_of_points
from dipy.align.streamlinear import compose_matrix44
from sklearn.neighbors import KDTree
from sklearn.decomposition import PCA


def make9D(bundles):
    cov = [[np.mean(i, axis=0), np.cov(i.T)] for i in bundles]
    return np.array([np.hstack((i, j[0], j[1, 1], j[1, 2], j[2, 2])) for i, j in cov])


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


def distance_kdTree9D(x0, static, moving):
    affine = compose_matrix44(x0)
    moving = transform_streamlines(moving, affine)

    new_static = make9D(static)
    new_moving = make9D(moving)

    tree = KDTree(new_moving)
    idx = np.hstack(tree.query(new_static, k=1)[1])

    moving = np.array(moving)[idx]
    cost = np.sum(np.linalg.norm(static - moving,axis=2))
    return cost


def pca_transform(static, moving,points=20):
    con_target = np.concatenate(static)
    con_subject = np.concatenate(moving)

    mean_s = np.mean(con_subject, axis=0)
    mean_t = np.mean(con_target, axis=0)

    pca = PCA(n_components=3)
    pca = pca.fit(con_subject)
    prev = pca.components_.T
    pca = pca.fit(con_target)

    aff = np.dot(prev, pca.components_)

    idx = [[],[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]]
    min = sys.maxsize
    for i in idx:
        aff2 = np.copy(aff)
        aff2[:, i] *= -1
        new_moving = [np.dot((i - mean_s), aff2) + mean_t for i in moving]
        moving_x = set_number_of_points(new_moving, points)
        static_x = set_number_of_points(static, points)
        cost = distance_kdTree9D([0, 0, 0], moving_x, static_x)
        # print(aff2,cost)
        if cost < min:
            new_move = new_moving
            min = cost
    # print(aff,min)
    del new_moving
    del min
    del pca
    del prev
    del mean_s
    del mean_t
    del con_target
    del con_subject
    del aff
    del aff2
    del moving_x
    del static_x
    return new_move
