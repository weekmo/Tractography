import numpy as np

idx = [[],[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]]
mat = np.array([[1,4,7],[2,5,8],[3,6,9]])
for i in idx:
    mat2 = np.copy(mat)
    mat2[:,i]*=-1
    print(mat2)