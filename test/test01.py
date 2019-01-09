# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:00:25 2018

@author: mabdelgadi
"""

from random import random
from time import time

import numpy as np

from sklearn.neighbors import KDTree
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from nibabel.affines import apply_affine
from dipy.tracking.streamline import set_number_of_points,transform_streamlines
from dipy.align.streamlinear import compose_matrix44
from dipy.core.optimize import Optimizer

#from src.tractography.Utils import transform
from src.tractography.viz import draw_bundles,draw_clusters,clusters_colors
from src.tractography.io import read_ply
'''
colors = [[random(),random(),random()] for _ in range(num)]

moving_clusters2 = clusters_colors(moving,colors,moving_clusters.labels_)
static_clusters2 = clusters_colors(static,colors,static_clusters.labels_)

draw_clusters([moving_clusters2,static_clusters2])

kdtree = KDTree(moving_clusters.cluster_centers_)
distances,ids = kdtree.query(np.concatenate(moving),k=num)
distances[distances==0]=1 #centroid distance must be 1
distances=1/distances
x0  = [compose_matrix44(np.multiply(np.reshape(dis,(num,1)),X1[id]).sum(axis=0)) for dis,id in zip(distances,ids)]
print(x0[-1])
'''
costs=[]
def cost_fun(x0,static_centers,moving_centers,max_dist):
    moving_centers = np.array([apply_affine(compose_matrix44(x),vec) for x,vec in zip(np.reshape(x0,(len(moving_centers),7)),moving_centers)])
    
    kdtree = KDTree(static_centers)
    #cost = kdtree.query(moving_centers,k=1)[0].sum()
    cost = kdtree.query(moving_centers,k=1)[0]
    cost = cost[np.where(cost < max_dist)].sum()
    costs.append(cost)
    return cost

def transform(affine,bundle,clusters_centers):
    num = len(clusters_centers)
    kdtree = KDTree(clusters_centers)
    distances,ids = kdtree.query(np.concatenate(bundle),k=num)
    distances[distances==0]=1 #centroid distance must be 1
    distances=1/distances  #heigh value for close verteces
    distances = np.divide(distances,distances.sum(axis=1).reshape((distances.shape[0],1)))
    # weights = distances[:,0]/distances.sum(axis=1) #The weigh is 
    affine  = [compose_matrix44(np.multiply(np.reshape(dis,(num,1)),affine[id]).sum(axis=0)) for dis,id in zip(distances,ids)]
    #Z = [apply_affine(compose_matrix44(np.multiply(np.reshape(dis,(num,1)),x0[id]).sum(axis=0)),vec) for dis,id,vec in zip(distances,ids,con_moving)]
    count = 0
    trans_bundle=[]
    for tract in bundle:
        temp = []
        for vec in tract:
            temp.append(apply_affine(affine[count],vec))
            count+=1
        trans_bundle.append(np.array(temp))
    return trans_bundle


static = read_ply('data/132118/m_ex_atr-right_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

#con_static = np.concatenate(static)
#con_moving = np.concatenate(moving)
num = 20
static_clusters = KMeans(n_clusters=num).fit(np.concatenate(static))
moving_clusters = KMeans(n_clusters=num).fit(np.concatenate(moving))


#x = np.array([[i,i,i,i,i,i,i] for i in range(1,9)])
x0 = np.array([[0,0,0, 0,0,0, 1] for _ in range(num)])

options = {'maxcor': 10, 'ftol': 1e-7,'gtol': 1e-5, 'eps': 1e-8}#,'maxiter': 10000000}#,'maxfun':200}

start = time()
m = Optimizer(cost_fun, x0,args=(static_clusters.cluster_centers_,moving_clusters.cluster_centers_,7),method='L-BFGS-B',options=options)
end = time()

m.print_summary()

#np.save('out/new_x0_00.npy',m.xopt)

x1 = np.reshape(m.xopt,(num,7))
new_moving = transform(x1,moving,moving_clusters.cluster_centers_)
draw_bundles([static,moving],[[1,0,0],[0,0,1]])
#draw_bundles([new_moving])


hours = int((end-start)/3600)
minutes = int(((end-start)%3600)/60)
seconds = int(((end-start)%3600)%60)

plt.plot(costs)
plt.title("Cost Function - Duration: {:02}:{}:{}\nMax dist: 7".format(hours,minutes,seconds))
plt.legend(['Distance','Link'])
plt.gray()
plt.savefig("pics/clust_cost_plot_000.png",dpi=600)

