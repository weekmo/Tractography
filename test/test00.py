
# x = [["a","b"], ["c"]]
# print([j for i in x for j in i])
import numpy as np
import sys
from random import random
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree
from sklearn.metrics.pairwise import paired_euclidean_distances

from scipy.sparse.linalg import lsqr
from scipy.sparse.linalg import LinearOperator
#from scipy.sparse import csc_matrix

from nibabel.affines import apply_affine
from dipy.core.optimize import Optimizer
from dipy.tracking.streamline import transform_streamlines, set_number_of_points
from dipy.align.streamlinear import compose_matrix44

from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles, clusters_colors, draw_clusters
from src.tractography.Utils import pca_transform_norm, normalize, kd_tree_cost, dist_new, costs

#static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('../data/150019/m_ex_atr-right_shore.ply')

#con_static = np.concatenate(static)
#con_moving = np.concatenate(moving)
        
def transform(moving,affines,length):
    assert np.min([len(i) for i in moving]) >= length
    assert len(affines) == length
    idx = [np.hstack(KDTree(j).query(i,k=1)[1]) for i,j in zip(set_number_of_points(moving,length),moving)]
    
    new_moving = []
    for tract_id in range(len(moving)):
        final_movie = []
        for i in range(len(affines)-1):
            length2 = idx[tract_id][i+1]-idx[tract_id][i]+1
            final_movie.append([apply_affine(compose_matrix44((((length2-j)/length2)*affines[i]) + ((j/length2)*affines[i+1])),moving[tract_id][j]) for j in range(length2)])
        new_moving.append(np.vstack(final_movie))
    return new_moving

def dist_new1(x0,sep_static,sep_moving,shape,r,max_dist,lam):
    affines = np.reshape(x0,shape)
    #con_moving = np.array([apply_affine(compose_matrix44(mat),s) for mat,s in zip(affines,con_moving)])
    con_moving = transform()
    
    dist_cost = kd_tree_cost(con_static,con_moving,max_dist)
    #print("dist",dist_cost)
    
    kdtree = KDTree(con_moving)
    idx = kdtree.query_radius(con_moving,r)

    stiff_cost = lam*np.sum([np.sum([np.linalg.norm(con_moving[i] - j) for j in con_moving[idx[i]]]) for i in range(len(con_moving))])
    #print("stiff",stiff_cost)
    costs.append([dist_cost,stiff_cost])
    return dist_cost+stiff_cost

length = 20
shape = (length,7)
affines = []
mat = np.array([20,20,20,180,180,120,1])
mats = np.array([[i,i,i, 0,0,0, 1] for i in range(length)])
for i in range(length):
    affines.append(mat.copy())
    mat[:-1] = mat[:-1]/1.01
test_new_moving = transform(moving,mats,length)
draw_bundles([moving])

length2 = 6

xx = [[((((length2-i)/length2)*mats[j]) + ((i/length2)*mats[j+1])) for i in range(length2)] for j in range(len(mats)-1)]

'''
options = {'maxcor': 10, 'ftol': 1e-7,'gtol': 1e-5, 'eps': 1e-8,'maxiter': 100000}

shape = (len(con_moving),len(x0[0]))
m = Optimizer(dist_new, x0,args=(con_static,con_moving,shape,.3,500),method='L-BFGS-B',options=options)
m.print_summary()
'''