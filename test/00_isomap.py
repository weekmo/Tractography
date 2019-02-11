#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 23:53:06 2019

@author: mohammed
"""

import sys
from os import path
sys.path.insert(0, path.abspath(path.curdir))

import numpy as np
from sklearn.manifold import Isomap
#from sklearn.decomposition import KernelPCA
from src.tractography.io import read_ply
from src.tractography.viz import isomap_lines_colors,draw_clusters

static = read_ply('data/197348/m_ex_atr-left_shore.ply')
#moving = read_ply('data/197348/m_ex_atr-right_shore.ply')

con_static = np.concatenate(static)
#con_moving = np.concatenate(moving)
'''
new_com = np.zeros((con_static.shape[0]+con_moving.shape[0],3))
new_com[:con_static.shape[0]] = con_static
new_com[con_static.shape[0]:] = con_moving

del static
del moving
del con_static
del con_moving
'''

iso = Isomap(n_components=1)
iso_original = iso.fit_transform(con_static)
iso_stat =iso_original-iso_original.min()
iso_stat = iso_stat/iso_stat.max()

iso_stat2 = np.zeros((iso_stat.shape[0],3))
iso_stat2[:,0] = iso_stat[:,0]
i = 0
end=0
colors=[]
for track in static:
    end = len(track)+i
    colors.append(iso_stat2[i:end-1])
    #new_moving.append([i,end])
    i = end
colored_bundle = isomap_lines_colors(static,colors)
draw_clusters([colored_bundle])
'''
print(iso_stat[-5:])
print(pca_stat[-5:])
'''
