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

from src.tractography.io import read_ply
from src.tractography.registration import register
from src.tractography.viz import draw_bundles

static = read_ply('data/197348/m_ex_atr-left_shore.ply') 
moving = read_ply('data/197348/m_ex_atr-right_shore.ply')

#con_static = np.concatenate(static)
con_static = np.concatenate(subject)
con_moving = np.concatenate(moving)

start = time()
new_moving = register(subject,moving)
end = time()

kdtree = KDTree(con_static)
distances = kdtree.query(np.concatenate(new_moving),k=1)[0]

hours   = int(( end - start)/3600)
minutes = int(((end - start)%3600)/60)
seconds = int(((end - start)%3600)%60)
print("Duration: {:02}:{:02}:{:02}".format(hours,minutes,seconds))
print("Total distance: {:2f}".format(distances.sum()))

#max_range = max(distances)
plt.hist(distances, bins='auto',range=(0,20))
plt.title("dipy | Duration: {:02}:{:02}:{:02}\nTotal Distance: {:2d}"
          .format(hours,minutes,seconds,np.sum(distances)))
plt.ylabel("Frequncy")
plt.xlabel("Distance")
plt.savefig('new_plan/{:02d}0_dipy_hist_original.png'.format(num), dpi=600)

draw_bundles([new_moving,subject],[[0,0,1],[1,0,0]])