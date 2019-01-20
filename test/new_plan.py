# -*- coding: utf-8 -*-
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import lsqr
from sklearn.neighbors import KDTree

from src.tractography.io import read_ply


static = read_ply('data/132118/m_ex_atr-right_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

''' Get points cloud '''
con_static = np.concatenate(static)
con_moving = np.concatenate(moving)

''' Vars '''
length = len(con_moving)
threshold=.9
alpha = 1
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
MG = sparse.kron(M,sparse.diags([1,1,1,lamb])).tocsr()
''' Get Zeros '''
zer = np.zeros((MG.shape[0],3))

A = sparse.vstack([MG,WD])
B = np.vstack([zer,WU])
''' --------------------- '''

X = np.array([lsqr(A,B[:,0])[0],
                   lsqr(A,B[:,1])[0],
                   lsqr(A,B[:,2])[0]]).T
