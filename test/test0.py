import numpy as np
from src.tractography.Utils import transform
from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles

#bundle = read_ply('../data/150019/m_ex_atr-right_shore.ply')
line = [np.array([[i,i,0] for i in range(200)]),np.array([[i,i,3] for i in range(200)])]
x0 = [[0,0,0, 0,0,0, 1],[2,2,2, 30,30,30, 1],[4,4,4, 60,60,60, 1],[6,6,6, 90,90,90, 1]]

#new_bundle = transform(x0,bundle)
new_line = transform(x0,line)

draw_bundles([new_line,line])
