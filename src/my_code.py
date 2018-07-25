'''
Created on 24 Jul 2018

@author: mohammed
'''
from plyfile import PlyData,PlyElement
#from os import listdir
#print(listdir("../data"))
ply_data = PlyData.read('../data/atr-left_shore.ply')
print(ply_data.elements[0].properties)