#!/usr/bin/python3.6
'''
Created on 24 Jul 2018

@author: mohammed
'''
#from shutil import copyfile

import numpy as np
from time import time
from dipy.tracking.streamline import transform_streamlines
from src.tractography.io import read_ply,write_trk,write_ply
from src.tractography.registration import register

data1 = read_ply('../data/132118/m_ex_atr-left_shore.ply')
data2 = read_ply('../data/132118/m_ex_atr-right_shore.ply')

'''Fake registration'''
mat = np.eye(4)

#mat = np.random.rand(4,4)*10
#mat[3,0],mat[3,1],mat[3,2],mat[3,3]=0,0,0,1
#print(mat)
#print(np.linalg.inv(mat))
new_sl = transform_streamlines(data1,mat)
#new_sl = data1.copy()
#write_ply('data/random_transformation.ply',new_sl)
#write_trk('data/random_transformation.trk',new_sl)
new_sl,mt=register(data1,new_sl)
new_sl,mt2=register(data1,new_sl)
#write_ply('data/realign_random.ply',new_sl)
#write_trk('data/realign_random.trk',new_sl)
#write_ply('data/terget.ply',data1)
print(mt,'\n',mt2)
print(abs(mt-mt2))
'''

new_sl=register(data1,data2)
write_ply('data/LTR_align.ply',new_sl)
write_trk('data/LTR_align.trk',new_sl)

write_ply('data/terget.ply',data1)
write_trk('data/target.trk',data1)
'''
'''
#register_all('data/')
# write_trk("../data/my_streamlines0.trk", data1)
r""" Test fake transformation matrix
mat = np.random.rand(4,4)*10
mat[3,0],mat[3,1],mat[3,2],mat[3,3]=0,0,0,1
print("Trans Mat:\n",mat)
test_same_bundle=transform_streamlines(data1,mat)

r""" Show
show_bundles([data1, test_same_bundle],
                  colors=[window.colors.orange, window.colors.blue],
                  show=False,
                  fname='../data/before_registration.png')

show_bundles([data1, after],
                  colors=[window.colors.orange, window.colors.blue],
                  show=False,
                  fname='../data/after_registration.png')
'''
