#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 08:05:05 2018

@author: mohammed
"""
'''
  W = nxn
  D = nx4x
  X = 4nx3
  U = nx3
  dist = |W(DX-U)|^2
'''
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import bicgstab,splu,lsqr

# W = sparse.csr_matrix(np.array([[1,0,0,0],[0,2,0,0],[0,0,3,0],[0,0,0,4]]))
W = np.diag([1,2,3,4,5,6,7,8,9,10])
I = sparse.identity(4)
K = sparse.kron(W,I)
print(D.toarray())

new_mov = moving[0][:10]
U = moving[0][90:100]

n = 10
j=0
dim=[]
for i in range(n):
    for _ in range(3):
        dim.append([i,j])
        j+=1
dim = np.array(dim)

old_mov = np.zeros((10,4))
old_mov[:,:3] = new_mov
old_mov[:,3] = [1 for _ in range(10)]
very_old = np.hstack(old_mov)

D = sparse.coo_matrix((very_old,(dim[:,0],dim[:,1])),shape=(n,n*4)).tocsr()
E = sparse.coo_matrix((np.hstack(new_mov),(dim[:,0],dim[:,1])),shape=(n,n*3)).tocsr()

x = moving[0][20:60]

W = sparse.csc_matrix(W)

A = W.dot(D)
print(E.shape,U.shape)
print(E.toarray())
x = lsqr(E,U)[0]