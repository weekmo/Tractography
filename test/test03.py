#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 23:53:06 2019

@author: mohammed
"""
from os import listdir  # , mkdir
from os.path import isfile  # , isdir

from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles


data_path = 'data/132118/'
files = [data_path + f for f in listdir(data_path) if isfile(data_path + f) and f.endswith('.ply')]

for i in files:
    print(i)

#static = read_ply('data/150019/m_ex_cst-right_shore.ply')