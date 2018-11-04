# import time
# import sys
# import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KDTree
# from sklearn.metrics.pairwise import euclidean_distances
# from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA
from src.tractography.io import read_ply
# from src.tractography.viz import draw_bundles
# from src.tractography.registration import registration_icp
# from open3d import draw_geometries
# from dipy.tracking.streamline import set_number_of_points
from src.tractography.viz import draw_bundles
from src.tractography.Utils import (kd_tree_cost,
                                    pca_transform_norm,
                                    distance_tract,
                                    distance_mdf)
from src.tractography.registration import registration_icp
from open3d import draw_geometries
from dipy.tracking.streamline import set_number_of_points
from dipy.align.bundlemin import distance_matrix_mdf
# from scipy.optimize import minimize

def select_threshold(static, moving):
    pca_moving = pca_transform_norm(static, moving, 20)

    con_static = np.concatenate(static)
    con_moving = np.concatenate(moving)
    con_pca_moving = np.concatenate(pca_moving)
    
    mean_m = np.mean(np.concatenate(moving), axis=0)
    mean_s = np.mean(np.concatenate(static), axis=0)
    moving_center = [i - mean_m + mean_s for i in moving]
    moving_center = np.concatenate(moving_center)
    
    tree = KDTree(moving_center)
    dist_before_PCA_centerd = np.hstack(tree.query(con_static, k=1)[0])

    tree = KDTree(con_moving)
    dist_before_PCA = np.hstack(tree.query(con_static, k=1)[0])

    tree = KDTree(con_pca_moving)
    dist_after_PCA = np.hstack(tree.query(con_static, k=1)[0])
    
    plt.hist(dist_before_PCA_centerd, bins='auto')
    plt.title("Distance before PCA - Centered (Moving is base)")
    plt.ylabel("Frequncy")
    plt.xlabel("Distance")
    plt.savefig('../pics/dist_before_PCA_centerd.png', dpi=600)
    plt.close()
    # plt.show()
    
    plt.hist(dist_before_PCA, bins='auto')
    plt.title("Distance before PCA (Moving is base)")
    plt.ylabel("Frequncy")
    plt.xlabel("Distance")
    plt.savefig('../pics/dist_before_PCA.png', dpi=600)
    plt.close()
    # plt.show()

    plt.hist(dist_after_PCA, bins='auto')
    plt.title("Distance After PCA (Moving is base) - distance < 20")
    plt.ylabel("Frequncy")
    plt.xlabel("Distance")
    plt.savefig('../pics/dist_after_PCA3.png', dpi=600)
    plt.close()
    # plt.show()

static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('../data/150019/m_ex_atr-right_shore.ply')
# select_threshold(static,moving)
