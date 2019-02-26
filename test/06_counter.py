# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 00:58:37 2019

@author: INSTHassaM3
"""
import numpy as np

import sys
from os import listdir  # , mkdir
from os.path import isfile  # , isdir

from src.tractography.io import read_ply

data_path = 'data/'

stat={}
max_bundles=0
min_bundles=sys.maxsize

max_points=0
min_points=sys.maxsize

for dirt in listdir(data_path):
    stat[dirt] = {}
    for bundle_path in listdir(data_path+dirt):
        bundle = read_ply(data_path+dirt+'/'+bundle_path)
        bundle_len = len(bundle)
        points_num = np.concatenate(bundle).shape[0]
        '''
        if bundle_len > max_bundles:
            max_bundles = bundle_len
        if bundle_len < min_bundles:
            min_bundles = bundle_len
            
        if points_num > max_points:
            max_points = points_num
        if points_num < min_points:
            min_points = points_num
        '''
        stat[dirt][bundle_path] = [bundle_len,points_num]
np.save('new_plan/bundles_statistic.npy',stat)

stat = np.load('new_plan/bundles_statistic.npy')

stat = stat[()]
with open('new_plan/data.csv','w') as f:
    for subject,bundles in stat.items():
        for bundle,vals in bundles.items():
            f.write(subject+','+bundle+','+str(vals[0])+','+str(vals[1])+'\n')


