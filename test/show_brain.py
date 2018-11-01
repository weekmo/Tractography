from src.tractography.viz import draw_bundles
from os import listdir  # , mkdir
from os.path import isfile  # , isdir
from src.tractography.io import read_ply
import argparse
from dipy.align.streamlinear import compose_matrix44
from dipy.tracking.streamline import transform_streamlines


parser = argparse.ArgumentParser(description='Input argument parser.')
parser.add_argument('-f', type=str, help='location of files')
args = parser.parse_args()
data_path = '../data/132118/'
#data_path = args.f
files = [data_path + f for f in listdir(data_path) if isfile(data_path + f) and f.endswith('.ply')]

mat = compose_matrix44([0,0,0,0,90,90])
brain = []
for name in files:
   brain.append(transform_streamlines(read_ply(name),mat))
draw_bundles(brain,rotate=True)

"""
data1 = read_ply('../data/132118/m_ex_atr-left_shore.ply')
data2 = read_ply('../data/132118/m_ex_atr-right_shore.ply')
draw_bundles([data1,data2])
"""