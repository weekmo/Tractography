#!/usr/bin/python3.6
'''
Created on 24 Jul 2018

@author: mohammed
'''
#from shutil import copyfile
import numpy as np
from dipy.tracking.streamline import transform_streamlines
from tractography.io import read_ply,write_trk,write_ply
from tractography.registration import register,register_all

data1 = read_ply('data/132118/m_ex_atr-left_shore.ply')
data2 = read_ply('data/132118/m_ex_atr-right_shore.ply')

'''Fake registration'''
mat = np.random.rand(4,4)*10
mat[3,0],mat[3,1],mat[3,2],mat[3,3]=0,0,0,1
new_sl = transform_streamlines(data1,mat)
new_sl=register(data1,new_sl)
write_ply('data/fake_align.ply',new_sl)
write_trk('data/fake_align.trk',new_sl)

''' Right to left'''
new_sl=register(data1,data2)
write_ply('data/fake_align.ply',new_sl)
write_trk('data/fake_align.trk',new_sl)

write_ply('data/terget.ply',data1)
write_trk('data/target.trk',data1)


register_all('data/')
# write_trk("../data/my_streamlines0.trk", data1)
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