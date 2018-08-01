'''
from os import listdir
from os.path import isfile,isdir,join
from tractographyPly import TractographyPly

data_path='../data'
files_names={}
for dir in listdir(data_path):
    ful_path=data_path+'/'+dir
    if isdir(ful_path):
        files_names[dir]=[f for f in listdir(ful_path) if isfile(ful_path+'/'+f)]

for k in files_names.keys():
    print(k)

tr = TractographyPly('../data/132118/m_ex_atr-left_shore.ply')
'''
from tractographyPly import TractographyPly,write_to_file
path1 = '../data/132118/m_ex_atr-left_shore.ply'
tract= TractographyPly(path1)
#write_to_file('../data/al.ply',tract.data,tract.indeces)