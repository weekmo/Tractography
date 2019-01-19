# -*- coding: utf-8 -*-
import numpy as np
from scipy import sparse
from sklearn.neighbors import KDTree
lsqr = sparse.linalg.lsqr

from src.tractography.io import read_ply


static = read_ply('data/132118/m_ex_atr-right_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

''' Get points cloud '''
con_static = np.concatenate(static)
con_moving = np.concatenate(moving)

''' Vars '''
length = len(con_moving)
threshold=.9
lamb = 1
''' Build KDTree '''
kdtree = KDTree(con_static)

''' Get Distances and indeces for closest points '''
dist,ids = kdtree.query(con_moving,k=1)
dist = np.concatenate(dist)
ids = np.concatenate(ids)
''' Get w by applying the threshold '''
# w = np.where(dist<threshold,0,1)
''' Make w diagonal '''
# W = sparse.diags(w)
W =sparse.diags(np.where(dist<threshold,0,1))
# I = sparse.identity(3)
# K = sparse.kron(W,I)
''' Moving in homogeneouse coordinates '''
new_con_moving = np.ones((length,4))
new_con_moving[:,:-1] = con_moving

D = sparse.coo_matrix((np.concatenate(new_con_moving),
                (np.repeat(np.arange(length),4),np.arange(length*4))),
                (length,length*4)).tocsr()

WD = W.dot(D)

U = con_static[ids]
WU = W.dot(U)
print(WU)


X = np.array([lsqr(WD,WU[:,0])[0],
                   lsqr(D,WU[:,1])[0],
                   lsqr(D,WU[:,2])[0]]).T

x0 = X[:4,:].T
x1 = x0[:,:-1]

v1 = np.dot(con_moving[0],x1)