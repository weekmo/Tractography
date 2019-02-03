# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 15:06:39 2018

@author: mabdelgadi
"""
import numpy as np

#import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree

from dipy.tracking.streamline import set_number_of_points

from src.tractography.viz import clusters_colors,draw_clusters,lines_colors
from src.tractography.io import read_ply

moving = read_ply('data/150019/m_ex_atr-left_shore.ply')


idx = [np.hstack(KDTree(j).query(i,k=1)[1]) for i,j in zip(set_number_of_points(moving,5),moving)]

xyz = lines_colors(moving,[[1,0,0],[0,1,0],[0,0,1],[1,0,1]],idx)
print(xyz)

con_moving = np.concatenate(moving)
mov_cluster = KMeans(n_clusters=5).fit(con_moving)

mov_cluster = clusters_colors(moving,[[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1]],mov_cluster.labels_)
draw_clusters(xyz)
