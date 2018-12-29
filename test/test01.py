# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:00:25 2018

@author: mabdelgadi
"""
import numpy as np
from random import random
from sklearn.neighbors import KDTree
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from nibabel.affines import apply_affine
from dipy.tracking.streamline import set_number_of_points,transform_streamlines
from dipy.align.streamlinear import compose_matrix44

from src.tractography.Utils import transform
from src.tractography.viz import draw_bundles,draw_clusters,clusters_colors
from src.tractography.io import read_ply

num = 8
static = read_ply('data/132118/m_ex_atr-right_shore.ply')
#static = transform_streamlines(static,compose_matrix44([30,0,0]))
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

static_clusters = KMeans(n_clusters=num).fit(np.concatenate(static))
moving_clusters = KMeans(n_clusters=num).fit(np.concatenate(moving))
'''
colors = [[random(),random(),random()] for _ in range(num)]

moving_clusters2 = clusters_colors(moving,colors,moving_clusters.labels_)
static_clusters2 = clusters_colors(static,colors,static_clusters.labels_)

draw_clusters([moving_clusters2,static_clusters2])
'''
'''
rep = np.array([0,1,3,2,6,3,1,0,9])
rep[rep==0] = 1
print(rep)
'''
kdtree = KDTree(static_clusters.cluster_centers_)
distances,ids = kdtree.query(np.concatenate(static),k=num)
distances[distances==0]=1 #centroid distance must be 1
distances=1/distances  #heigh value for close verteces
weights = distances[:,0]/distances.sum(axis=1) #The weigh is 
print(distances[0][0]/distances.sum(axis=1)[0])
print(distances.sum(axis=1))
#print(ids[234])
#print(static_clusters.labels_[234])

x = np.array([[1,2],[3,4],[5,6]])
print(np.multiply(x,x))
