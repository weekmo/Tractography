# -*- coding: utf-8 -*-

from time import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import lsqr
from sklearn.neighbors import KDTree

import matplotlib.pyplot as plt

from src.tractography.io import read_ply
from src.tractography.Utils import pca_transform_norm
from src.tractography.viz import draw_bundles


static = read_ply('data/132118/m_ex_atr-right_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

''' Get points cloud '''
con_static = np.concatenate(static)
con_moving = np.concatenate(moving)

''' Build KDTree '''
kdtree = KDTree(con_static)

''' Get the threshold '''
plt.hist(kdtree.query(con_moving,k=1)[0], bins='auto')
plt.title("Distance before PCA")
plt.ylabel("Frequncy")
plt.xlabel("Distance")
plt.savefig('new_plan/dist_before_PCA.png', dpi=600)

''' Apply PCA '''
con_moving = np.concatenate(pca_transform_norm(static,moving))

''' Get the threshold '''
plt.hist(kdtree.query(con_moving,k=1)[0], bins='auto')
plt.title("Distance after PCA")
plt.ylabel("Frequncy")
plt.xlabel("Distance")
plt.savefig('new_plan/dist_after_PCA.png', dpi=600)

''' Vars '''
length = len(con_moving)
threshold=.4
alpha = 1
lamb = 1

''' Get Distances and indeces for closest points '''
dist,ids = kdtree.query(con_moving,k=1)
dist = np.concatenate(dist)
ids = np.concatenate(ids)
''' Get w by applying the threshold '''
# w = np.where(dist<threshold,0,1)
''' Make w diagonal '''
# W = sparse.diags(w)
'''
x =np.where(dist<threshold,0,1)
print(np.unique(x,return_counts=True))
'''
W = sparse.diags(np.where(dist<threshold,0,1))
# I = sparse.identity(3)
# K = sparse.kron(W,I)
''' Moving in homogeneouse coordinates '''
new_con_moving = np.ones((length,4))
new_con_moving[:,:-1] = con_moving

D = sparse.coo_matrix((np.concatenate(new_con_moving),
                (np.repeat(np.arange(length),4),np.arange(length*4))),
                (length,length*4)).tocsr()
''' Get WD '''
WD = W.dot(D)
''' Get U '''
# U = con_static[ids]
''' Get WD '''
WU = W.dot(con_static[ids])

''' Stiffnes '''
length = con_moving.shape[0]-len(moving)
data = np.tile([-1,1],length)
row = np.arange(length).repeat(2)

col=[]
j=0
for track in moving:
    end = j+track.shape[0]
    col.append(np.arange(j,end).repeat(2)[1:-1])
    j = end
col = np.concatenate(col)

M = sparse.csr_matrix((data,(row,col)),(length,con_moving.shape[0]))

''' Get G '''
# G = sparse.diags([1,1,1,lamb])
MG = alpha*sparse.kron(M,sparse.diags([1,1,1,lamb])).tocsr()
''' Get Zeros '''
zer = np.zeros((MG.shape[0],3))

A = sparse.vstack([MG,WD])
B = np.vstack([zer,WU])

start = time()
X = np.array([lsqr(A,B[:,0])[0],
                   lsqr(A,B[:,1])[0],
                   lsqr(A,B[:,2])[0]]).T
end = time()

np.save('new_plan/x0.npy',X)

hours = int((end-start)/3600)
minutes = int(((end-start)%3600)/60)
seconds = int(((end-start)%3600)%60)
print("Duration: {:02}:{}:{}".format(hours,minutes,seconds))

new_con_mov=D.dot(X)

i = 0
end=0
new_moving=[]
for track in moving:
    end = len(track)+i
    new_moving.append(new_con_mov[i:end])
    #new_moving.append([i,end])
    i = end
    
draw_bundles([moving, new_moving])

