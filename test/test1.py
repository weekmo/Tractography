# import time
import sys
# import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KDTree
# from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA
from src.tractography.io import read_ply
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
def select_threshold(static,moving):

    new_moving = pca_transform_norm(static, moving, 50)
    
    con_static = np.concatenate(static)
    con_moving = np.concatenate(moving)
    con_new_moving = np.concatenate(new_moving)
    
    tree = KDTree(con_moving)
    dist_before_PCA = np.hstack(tree.query(con_static, k=1)[0])
    
    tree = KDTree(con_new_moving)
    dist_after_PCA = np.hstack(tree.query(con_static, k=1)[0])
    
    
    plt.hist(dist_before_PCA,bins='auto')
    plt.title("Distance before PCA (Moving is base)")
    plt.ylabel("Frequncy")
    plt.xlabel("Distance")
    plt.savefig('dist_before_PCA2.png', dpi=600)
    plt.close()
    #plt.show()
    
    plt.hist(dist_after_PCA,bins='auto')
    plt.title("Distance After PCA (Moving is base)")
    plt.ylabel("Frequncy")
    plt.xlabel("Distance")
    plt.savefig('dist_after_PCA2.png', dpi=600)
    #plt.show()
print(distance_mdf([0,0,0],static_points,moving_points))
print(distance_tract([0,0,0],static_points,moving_points,500))

static = read_ply('data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

#select_threshold(static,moving)