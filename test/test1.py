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
from src.tractography.Utils import kd_tree_cost, pca_transform_norm
from src.tractography.registration import registration_icp
from open3d import draw_geometries
from dipy.tracking.streamline import set_number_of_points
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

def dist_tract(static,moving,points,min_dist):
    points = 10
    min_dist = 40
    static_points = set_number_of_points(static,points)
    moving_points = set_number_of_points(moving,points)
    #idx =[]
    total_cost = 0
    for i in static_points:
        min_cost=sys.maxsize
        #index = -1
        #for k,j in enumerate(moving_points):
        for j in moving_points:
            cost1 = np.linalg.norm(i - j,axis=1)
            cost1 = np.sum(cost1[np.where(cost1<min_dist)])
            
            cost2 = np.linalg.norm(i - j[::-1],axis=1)
            cost2 = np.sum(cost2[np.where(cost2<min_dist)])
            
            cost = np.min([cost1,cost2])
            if cost<min_cost:
                min_cost = cost
                #index = k
        total_cost+=min_cost
        #idx.append(index)
    
x = np.linalg.norm(static_points[0] - moving_points[0],axis=1)
x_con = np.sum(x[np.where(x<40)])
print(x_con)
static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('../data/150019/m_ex_atr-right_shore.ply')

#select_threshold(static,moving)