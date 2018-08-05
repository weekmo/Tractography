'''
Created on 24 Jul 2018

@author: mohammed
'''
from tractographyPly import read,write,show_bundles,register,register_all
from dipy.viz import window
#register_all('../data/')
aligned_bundle=register(traget_path= '../data/150019/m_ex_atr-left_shore.ply',
                        subject_path='../data/164939/m_ex_atr-left_shore.ply')

data1 = read('../data/150019/m_ex_atr-left_shore.ply')
data2 = read('../data/164939/m_ex_atr-left_shore.ply')
write('../data/test.ply',aligned_bundle)
show_bundles([data1, data2,aligned_bundle],
                  colors=[window.colors.orange, window.colors.red,window.colors.blue],
                  show=False,
                  fname='../data/before_registration.png')
"""
show_bundles([data1, aligned_bundle],
                  colors=[window.colors.orange, window.colors.red],
                  show=False,
                  fname='../data/after_registration.png')
"""