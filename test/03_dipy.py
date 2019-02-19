#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 17:54:32 2019

@author: mohammed
"""
from time import time

import numpy as np
from sklearn.neighbors import KDTree

import matplotlib.pyplot as plt

from dipy.tracking.streamline import transform_streamlines

from src.tractography.io import read_ply
from src.tractography.Utils import pca_transform_norm,flip
from src.tractography.registration import register
from src.tractography.viz import draw_bundles

static = read_ply('data/197348/m_ex_atr-left_shore.ply') 
moving = read_ply('data/197348/m_ex_atr-right_shore.ply')

''' Apply PCA '''
pre_moving = pca_transform_norm(static, moving, best=True)
draw_bundles([pre_moving,static],[[0,0,1],[1,0,0]])

''' Flip '''
'''
pre_moving = flip(moving,x=-1)
draw_bundles([pre_moving,static],[[0,0,1],[1,0,0]])
'''

con_static = np.concatenate(static)
con_moving = np.concatenate(pre_moving)

start = time()
new_moving = register(static,pre_moving)
end = time()

kdtree = KDTree(con_static)
distances = kdtree.query(np.concatenate(new_moving),k=1)[0]

hours   = int(( end - start)/3600)
minutes = int(((end - start)%3600)/60)
seconds = int(((end - start)%3600)%60)
print("Duration: {:02}:{:02}:{:02}".format(hours,minutes,seconds))
print("Total distance: {:2f}".format(distances.sum()))

#max_range = max(distances)
plt.hist(distances, bins='auto',range=(0,max_range))
plt.title("dipy | Duration: {:02}:{:02}:{:02}\nTotal Distance: {:}"
          .format(hours,minutes,seconds,round(distances.sum(),2)))
plt.ylabel("Frequncy")
plt.xlabel("Distance")
plt.savefig('new_plan/1{:02d}_dipy_hist.png'.format(num), dpi=600)

draw_bundles([new_moving,static],[[0,0,1],[1,0,0]])