
from os import listdir,mkdir
from os.path import isfile,isdir,join
from my_code import register
from tractographyPly import show_both_bundles,write_to_file
data_path='../data/'
files_names={}
for dir in listdir(data_path):
    dir=data_path+dir+'/'
    if isdir(dir):
        files_names[dir]=[f for f in listdir(dir) if isfile(dir+f)]

index=0
for k in files_names.keys():
    if index ==0:
        target_key=k
    else:
        output_path=k[:-1]+'_output/'
        if not isdir(output_path):
            mkdir(output_path)
        for target_path,subject_path in zip(files_names[target_key],files_names[k]):
            if target_path == subject_path:
                aligned_subject=register(target_key+target_path,k+subject_path)
                write_to_file(output_path+subject_path,aligned_subject)
    index+=1