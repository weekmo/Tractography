#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 23:53:06 2019

@author: mohammed
"""
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

test = 3*sparse.csr_matrix(([1,2,3,4],([0,1,2,2],[0,1,2,3])),(3,4))
test = 3*test
print(test.toarray())
