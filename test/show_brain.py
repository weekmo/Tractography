from src.tractography.viz import draw_brain
from os import listdir  # , mkdir
from os.path import isfile  # , isdir
from tractography.io import read_ply
import argparse

parser = argparse.ArgumentParser(description='Input argument parser.')
parser.add_argument('-f', type=str, help='location of files')
args = parser.parse_args()
# data_path = '../data/132118/'
data_path = args.f
files = [data_path + f for f in listdir(data_path) if isfile(data_path + f) and f.endswith('.ply')]

brain = []
for name in files:
    brain.append(read_ply(name))
draw_brain(brain)