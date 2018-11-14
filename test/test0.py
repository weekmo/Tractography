
# x = [["a","b"], ["c"]]
# print([j for i in x for j in i])
import numpy as np
from sklearn.neighbors import KDTree

#from scipy.sparse.linalg import lsqr
#from scipy.sparse import csc_matrix
from nibabel.affines import apply_affine
from dipy.tracking.streamline import transform_streamlines,set_number_of_points
from dipy.align.streamlinear import compose_matrix44

from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles
from src.tractography.Utils import kd_tree_cost




def dist_new(x0,sep_static,sep_moving,shape,max_dist):
    affines = np.reshape(x0,shape)
    con_moving = np.array([apply_affine(compose_matrix44(mat),s) for mat,s in zip(affines,sep_moving)])
    
    dist_cost = kd_tree_cost(np.concatenate(sep_static),np.concatenate(con_moving),max_dist)
    return dist_cost

shape = (20,7)

sep_static = set_number_of_points(static,shape[0])
sep_moving = set_number_of_points(moving,shape[0])

x0 = [[0,0,0, 0,0,0, 1] for _ in range(shape[0])]

print(dist_new(x0,sep_static,sep_moving,shape,500))
