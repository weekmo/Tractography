#!/usr/bin/python3.6
'''
Created on 24 Jul 2018

@author: mohammed
'''
# from dipy.tracking.streamline import transform_streamlines
from src.tractography.io import read_ply,write_trk
from src.tractography.registration import register_all

# data1 = read_ply('../data/132118/m_ex_atr-left_shore.ply')
# data2 = read_ply('../data/150019/m_ex_atr-left_shore.ply')

# register_all('../data/')
# write_trk("../data/my_streamlines1.trk", data1)
r""" Test fake transformation matrix
mat = np.random.rand(4,4)*10
mat[3,0],mat[3,1],mat[3,2],mat[3,3]=0,0,0,1
print("Trans Mat:\n",mat)
test_same_bundle=transform_streamlines(data1,mat)
"""
r""" Show
show_bundles([data1, test_same_bundle],
                  colors=[window.colors.orange, window.colors.blue],
                  show=False,
                  fname='../data/before_registration.png')

show_bundles([data1, after],
                  colors=[window.colors.orange, window.colors.blue],
                  show=False,
                  fname='../data/after_registration.png')
"""