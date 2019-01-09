# x = [["a","b"], ["c"]]
# print([j for i in x for j in i])

from time import time
import numpy as np
#import sys
#from random import random

import matplotlib.pyplot as plt

#from sklearn.cluster import KMeans
#from sklearn.neighbors import KDTree
#from sklearn.metrics.pairwise import paired_euclidean_distances

#from scipy.sparse.linalg import lsqr
#from scipy.sparse.linalg import LinearOperator
#from scipy.sparse import csc_matrix

#from nibabel.affines import apply_affine
from dipy.core.optimize import Optimizer
#from dipy.tracking.streamline import transform_streamlines, set_number_of_points
#from dipy.align.streamlinear import compose_matrix44

from src.tractography.io import read_ply
#from src.tractography.viz import draw_bundles
from src.tractography.Utils import costs, transform,dist_new,pca_transform_norm, link_cost



static = read_ply('data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('data/150019/m_ex_atr-left_shore.ply')

pca_moving = pca_transform_norm(static,moving,5000)

length = 5
x0 = np.array([[0,0,0, 0,0,0, 1] for _ in range(length)])
lnk_cost = link_cost(transform(x0,pca_moving))
options = {'maxcor': 10, 'ftol': 1e-7,
           'gtol': 1e-5, 'eps': 1e-8,
           'maxiter': 1000}#,'maxfun':200}

start = time()
m = Optimizer(dist_new, x0,args=(static,pca_moving,length,lnk_cost,50,10),method='L-BFGS-B',options=options)
end = time()

m.print_summary()

np.save('out/dist_link11.npy',m.xopt)
np.save('out/costs11.npy',costs)

x1 = np.reshape(m.xopt,(5,7))
new_moving = transform(x1,moving)
#draw_bundles([moving,new_moving],[[1,0,0],[0,0,1]])
#draw_bundles([new_moving])


hours = int((end-start)/3600)
minutes = int(((end-start)%3600)/60)
seconds = int(((end-start)%3600)%60)

plt.plot(costs)
plt.title("Cost Function - Duration: {:02}:{}:{}\nLambda: 10, Max dist: 50".format(hours,minutes,seconds))
plt.legend(['Distance','Link'])
plt.gray()
plt.savefig("pics/cost_plot11.png",dpi=600)

'''
plt.plot(costs[2735:2773])
plt.plot(costs[:2736])
plt.plot(costs[2772:])
new_cost = np.vstack([costs[:2736],costs[2772:]])
plt.plot(new_cost)
'''