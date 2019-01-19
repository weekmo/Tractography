#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 23:53:06 2019

@author: mohammed
"""

test = np.tile([-1,1],4)
test2 = np.repeat([-1,1],4).reshape((2,4))

print(sparse.diags(test2,[0,1]).toarray())