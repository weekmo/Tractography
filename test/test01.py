# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:00:25 2018

@author: mabdelgadi
"""
import numpy as np
from sklearn.neighbors import KDTree

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from nibabel.affines import apply_affine
from dipy.tracking.streamline import set_number_of_points
from dipy.align.streamlinear import compose_matrix44

from src.tractography.Utils import transform
from src.tractography.viz import draw_bundles
from src.tractography.io import read_ply

num = 5
#static = read_ply('data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

xaxis = np.array([[i,0,0] for i in range(num)])
yaxis = np.array([[0,i,0] for i in range(num)])
zaxis = np.array([[0,0,i] for i in range(num)])
axis = [xaxis,yaxis,zaxis]
bundle = [np.array([[i,i,i] for i in range(num)])]
x0 = [[0,0,0, i,i,i, 1] for i in range(0,360,30)]
new_bundle = transform(x0,bundle)
#draw_bundles([axis,bundle])
draw_bundles([axis,bundle,new_bundle],[[1,0,0],[0,0,1],[0,1,0]])

idx = [np.hstack(KDTree(j).query(i,k=1)[1]) for i,j in zip(set_number_of_points(bundle,len(x0)),bundle)][0]

temp = []
index = 0
for k in range(len(x0)-1):
    length2 = idx[k+1]-idx[k]
    j=0
    for index in range(idx[k],idx[k+1]):
        mat1 = np.copy(x0[k]).astype(float)
        mat1[:-1] = ((length2-j)/length2)*mat1[:-1]
        
        mat2 = np.copy(x0[k+1]).astype(float)
        mat2[:-1] = (j/length2)*mat2[:-1]
        
        mat3 = np.zeros((7,))
        mat3[:-1] = mat2[:-1]+mat1[:-1]
        mat3[-1] = mat2[-1]*mat1[-1]
        
        temp.append(apply_affine(compose_matrix44(mat3),bundle[0][index]))
        j+=1
        index+=1
np.vstack(temp)