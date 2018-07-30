'''
Created on 24 Jul 2018

@author: mohammed
'''

'''
import plyStruct as ps
path = '../data/132118/m_ex_atr-left_shore.ply'

#ply_data = PlyData.read(path)
my_ply = ps.plyStruct()
my_ply.loadPolyData(path)
print(my_ply.idx)
print(my_ply.feDict['x_idx'][:10])
print(my_ply.feDict['x'][:10])
print(my_ply.feDict['x'][0]-my_ply.feDict['x_idx'][0])
print(my_ply.feDict['x'][1]-my_ply.feDict['x_idx'][1])
print(my_ply.feDict['x'][2]-my_ply.feDict['x_idx'][2])
'''
#from plyfile import PlyData, PlyElement
from dipy.tracking.streamline import set_number_of_points
from dipy.io import Dpy
#path = '../data/134223/atr-left_tckgen.ply'
path = 'test.ply'
x=Dpy(path)