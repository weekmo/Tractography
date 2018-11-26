# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 15:06:39 2018

@author: mabdelgadi
"""
import numpy as np
from nibabel.affines import apply_affine
from dipy.align.streamlinear import compose_matrix44

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from src.tractography.viz import draw_bundles
from src.tractography.io import read_ply

moving = read_ply('data/150019/m_ex_atr-right_shore.ply')
static = read_ply('data/132118/m_ex_atr-left_shore.ply')

xyz=np.array([[i,i,i] for i in range(5)])
aff = [compose_matrix44([0,0,0, i,i,i]) for i in range(0,150,30)]

new_xyz = np.array([apply_affine(f,p) for f,p in zip(aff,xyz)])



fig = plt.figure()
ax = fig.gca(projection='3d')
for tract in moving:
    ax.plot(tract[:,0],tract[:,1],tract[:,2],color='blue')
for tract in static:
    ax.plot(tract[:,0],tract[:,1],tract[:,2],color='red')
plt.savefig("3d.png",dpi=600)