'''
Created on 24 Jul 2018

@author: mohammed
'''
from plyfile import PlyData, PlyElement
import playStruct as ps

path = '../data/134223/atr-left_tckgen.ply'
# ply_data = PlyData.read(path)
my_ply = ps.plyStruct()
my_ply.loadPolyData(path)
#print(my_ply.idx)
print(my_ply.feDict['x_idx'][:10])
print(my_ply.feDict['x'][:10])