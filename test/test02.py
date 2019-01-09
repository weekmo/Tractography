#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 17:54:32 2019

@author: mohammed
"""
import numpy as np
from scipy import sparse as sp

a = np.repeat(np.array([[1,2,3],[4,5,6],[7,8,9]]),4).reshape((4,3,3))
b = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]]).T

c = np.dot(b,a)

print(np.concatenate(a))
print(b[0])
print(c[0])

print(np.dot(b[0],a[0]))