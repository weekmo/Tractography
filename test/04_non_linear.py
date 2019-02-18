#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 18:34:22 2019

@author: mohammed
"""
from time import time

import numpy as np
from sklearn.neighbors import KDTree

from dipy.core.optimize import Optimizer
from dipy.tracking.streamline import transform_streamlines
from dipy.align.streamlinear import compose_matrix44

import matplotlib.pyplot as plt

from src.tractography.Utils import pca_transform_norm, distance_pc
from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles


static = read_ply('data/197348/m_ex_atr-left_shore.ply')
moving = read_ply('data/197348/m_ex_atr-right_shore.ply')

pca_moving = pca_transform_norm(static,moving)

max_range = 46
x0 = [0,0,0, 0,0,0, 1]
options = {'maxcor': 10, 'ftol': 1e-7,'gtol': 1e-5, 'eps': 1e-8,'maxiter': 1000}

start = time()
m = Optimizer(distance_pc, x0,args=(static,pca_moving,1,50),method='L-BFGS-B',options=options)
end = time()

aff = compose_matrix44(m.xopt)
new_moving = transform_streamlines(pca_moving,aff)
draw_bundles([new_moving,static],[[0,0,1],[1,0,0]])

''' Build KDTree '''
kdtree = KDTree(np.concatenate(static))
distances = kdtree.query(np.concatenate(new_moving),k=1)[0]

hours   = int(( end - start)/3600)
minutes = int(((end - start)%3600)/60)
seconds = int(((end - start)%3600)%60)
print("Duration: {:02}:{}:{}".format(hours,minutes,seconds))

''' Get the threshold '''
#max_range = max(distances)
plt.hist(distances, bins='auto',range=(0,max_range))
plt.title("Non Linear Method (optimizer) | Duration: {:02}:{:02}:{:02}".format(hours,minutes,seconds)+
          "\nTotal distance: {:}".format(round(distances.sum(),2)))
plt.ylabel("Frequncy")
plt.xlabel("Distance")
plt.savefig('new_plan/{:02d}0_hist_nonlinear.png'.format(num), dpi=600)
