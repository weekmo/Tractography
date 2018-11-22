# x = [["a","b"], ["c"]]
# print([j for i in x for j in i])

from time import time
import numpy as np
import sys
from random import random

import matplotlib.pyplot as plt

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
from src.tractography.Utils import costs, transform,dist_new

static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('../data/150019/m_ex_atr-right_shore.ply')

#con_static = np.concatenate(static)
#con_moving = np.concatenate(moving)

length = 2
x0 = np.array([[0,0,0, 0,0,0, 1] for _ in range(length)])
options = {'maxcor': 10, 'ftol': 1e-7, 'gtol': 1e-5, 'eps': 1e-8, 'maxiter': 1000}
start = time()
m = Optimizer(dist_new, x0,args=(static,moving,length,500,70),method='L-BFGS-B',options=options)
end = time()

#print("Time: ",end-start)
m.print_summary()
np.save('../out/dist_link3.npy',m.xopt)
x1 = np.reshape(m.xopt,(2,7))
new_moving = transform(x1,moving)
draw_bundles([new_moving])
draw_bundles([static,new_moving],[[1,0,0],[0,0,1]])

hours = int((end-start)/3600)
minutes = int(((end-start)%3600)/60)
seconds = int(((end-start)%3600)%60)

plt.plot(costs)
plt.title("Cost Function (Dist and Link)\nTime: {:02}:{}:{}, Maxiter=1000, lambda=70".format(hours,minutes,seconds))
plt.legend(['Distance','Link'])
plt.savefig("../pics/21-11-2018/cost_plot5.png",dpi=600)
