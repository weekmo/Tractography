import numpy as np
import sys
from src.tractography.io import read_ply
from src.tractography.Utils import pca_transform, distance_kdTree9D
from src.tractography.viz import draw_brain
from src.tractography.registration import registration_icp,register
from sklearn.neighbors import KDTree
from dipy.tracking.streamline import set_number_of_points,transform_streamlines
from dipy.align.streamlinear import compose_matrix44
from sklearn.decomposition import PCA

# TODO Get 9D vector for each tract using cov matrix

static = read_ply('../data/197348/m_ex_atr-left_shore.ply')
moving = read_ply('../data/164939/m_ex_atr-left_shore.ply')

new_move = registration_icp(static,moving,pca=False)
new_move2 = register(static,moving)
draw_brain([static,moving,new_move,new_move2],[[1,0,0],[0,0,1],[1,1,0],[0,1,0]])
# TODO Measure the distance using KDTree
