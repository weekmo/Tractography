import numpy as np
import sys

from dipy.segment.quickbundles import bundles_distances_mdf
from dipy.tracking.streamline import transform_streamlines
from dipy.align.streamlinear import compose_matrix44

from sklearn.neighbors import KDTree
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from pyclustering.cluster.kmedoids import kmedoids


def make9D(bundles):
    cov = [[np.mean(i, axis=0), np.cov(i.T)] for i in bundles]
    return np.array([np.hstack((i, j[0], j[1, 1], j[1, 2], j[2, 2])) for i, j in cov])


def normalize(bundle):
    calc_bundle = np.min(np.concatenate(bundle))
    new_bundle = [i - calc_bundle for i in bundle]
    calc_bundle = np.max(np.concatenate(new_bundle))
    new_bundle = [i / calc_bundle for i in new_bundle]
    return new_bundle


def kd_tree_cost(static, moving, max_dist):
    tree = KDTree(moving)
    dist_list = np.hstack(tree.query(static, k=1)[0])
    return np.sum(dist_list[np.where(dist_list < max_dist)])


def distance_mdf(x0, static, moving):
    # Minimum Direct Flip (MDF) distance
    aff = compose_matrix44(x0)
    moving = transform_streamlines(moving, aff)
    dist_mat = bundles_distances_mdf(static, moving)
    # idx = np.argmin(dist_mat, axis=1)
    cost = np.sum(np.min(dist_mat, axis=1))
    return cost


def distance_tract(x0,static,moving,min_dist):
    """
    MDF implementation usning SUM (not mean)
    """
    aff = compose_matrix44(x0)
    moving = transform_streamlines(moving, aff)
    #idx =[]
    total_cost = 0
    for i in static:
        min_cost=sys.maxsize
        #index = -1
        #for k,j in enumerate(moving_points):
        for j in moving:
            cost1 = np.linalg.norm(i - j,axis=1)
            cost1 = np.sum(cost1[np.where(cost1<min_dist)])
            
            cost2 = np.linalg.norm(i - j[::-1],axis=1)
            cost2 = np.sum(cost2[np.where(cost2<min_dist)])
            
            cost = np.min([cost1,cost2])
            if cost<min_cost:
                min_cost = cost
                #index = k
        total_cost+=min_cost
    return total_cost


# It uses point cloud
def distance_kdtree(x0, static, moving, beta, max_dist):
    # joint bundles
    affine = compose_matrix44(x0)
    moving = transform_streamlines(moving, affine)
    return kd_tree_cost(np.concatenate(static), np.concatenate(moving), max_dist) * beta


# It uses tracts distance
def distance_kdTree9D(x0, static, moving, beta, max_dist):
    affine = compose_matrix44(x0)
    moving = transform_streamlines(moving, affine)

    new_static = make9D(static)
    new_moving = make9D(moving)

    return kd_tree_cost(new_static, new_moving, max_dist) * beta


class Clustering:

    def __init__(self):
        self.inint_dist = np.zeros((3, 3))
        self.clustering = True

    """
    Use point cloud
    """

    def distance_pc_clustering_medoids(self, x0, static, moving, medoids, beta, max_dist):
        affine = compose_matrix44(x0)
        moving = transform_streamlines(moving, affine)

        con_static = np.concatenate(static)
        con_moving = np.concatenate(moving)

        # con_static = static
        # con_moving=moving

        tree = KDTree(con_moving)
        dist_list = np.hstack(tree.query(con_static, k=1)[0])
        cost = np.sum(dist_list[np.where(dist_list < max_dist)])

        if self.clustering:
            self.kmedoids = kmedoids(con_moving, medoids)
            self.kmedoids.process()
            self.clustering = False

        clustering_cost = 0
        for i in range(len(medoids)):
            mean = np.mean(con_moving[self.kmedoids.get_clusters()[i]], axis=0)
            clustering_cost += np.linalg.norm(con_moving[self.kmedoids.get_medoids()[i]] -
                                              con_moving[tree.query([mean], k=1)[1][0]][0])
        return cost + beta * clustering_cost

    def distance_pc_clustering_mean(self, x0, static, moving, k, beta, max_dist):
        """
        Clustering once
        :param x0:
        :param static:
        :param moving:
        :param c_num:
        :param k:
        :return:
        """
        affine = compose_matrix44(x0)
        moving = transform_streamlines(moving, affine)

        con_static = np.concatenate(static)
        con_moving = np.concatenate(moving)

        cost = kd_tree_cost(con_static, con_moving, max_dist)

        if self.clustering:
            self.kmeans = KMeans(k).fit(con_moving)
            self.idx = {i: np.where(self.kmeans.labels_ == i)[0] for i in range(k)}
            self.clustering = False

        clustering_cost = 0
        for i in range(k):
            clustering_cost += np.linalg.norm(
                self.kmeans.cluster_centers_[i] - np.mean(con_moving[self.idx[i]], axis=0))
        return cost + beta * clustering_cost


def pca_transform_norm(static, moving, max_dist):
    con_static = np.concatenate(static)
    con_moving = np.concatenate(moving)

    mean_static = np.mean(con_static, axis=0)
    mean_moving = np.mean(con_moving, axis=0)

    norm_static = normalize(static)
    norm_moving = normalize(moving)

    con_norm_static = np.concatenate(norm_static)
    con_norm_moving = np.concatenate(norm_moving)

    norm_static_mean = np.mean(con_norm_static, axis=0)
    norm_moving_mean = np.mean(con_norm_moving, axis=0)

    pca = PCA(n_components=3)
    pca = pca.fit(con_moving)
    prev = pca.components_.T
    pca = pca.fit(con_static)

    aff = np.dot(prev, pca.components_)

    idx = [[], [0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]
    min = sys.maxsize
    for i in idx:
        aff2 = np.copy(aff)
        aff2[:, i] *= -1
        new_moving = [np.dot((j - norm_moving_mean), aff2) + norm_static_mean for j in norm_moving]
        cost = kd_tree_cost(con_norm_static, np.concatenate(new_moving), max_dist)
        # print(cost)
        if cost < min:
            new_aff = aff2
            min = cost
    new_move = [np.dot((j - mean_moving), new_aff) + mean_static for j in moving]
    # print(min)
    del new_moving
    del min
    del pca
    del prev
    del mean_moving
    del mean_static
    del con_static
    del con_moving
    del aff
    del aff2
    return new_move
