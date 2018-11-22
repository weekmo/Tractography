import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import lsqr
from dipy.tracking.streamline import set_number_of_points
from src.tractography.io import read_ply

bundle= read_ply('../data/150019/m_ex_atr-right_shore.ply')
bundle = set_number_of_points(bundle,20)

d = bundle[0]
len_d = len(d)

dim = []
j=0
for i in range(len_d):
    for _ in range(3):
        dim.append([i,j])
        j+=1

dim=np.array(dim)
shape=(len_d,len_d*3)
D = coo_matrix((np.concatenate(d),(dim[:,0],dim[:,1])),shape=shape).tocsr()
U = np.concatenate(bundle[180])

print(D.shape)
print(U.shape)

x = lsqr(D.T,U)[0]
print(x)