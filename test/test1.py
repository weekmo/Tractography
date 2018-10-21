import numpy as np
from sklearn.neighbors import KDTree
from sklearn.metrics.pairwise import euclidean_distances

init_dist = np.zeros((3,3))
mat = np.array([[1,4,7],[2,5,8],[3,6,9]])
mat1 = np.array([[3,0,0],[6,0,0],[0,0,0]])
mat2 = np.array([[0,6,0],[0,8,0],[0,0,0]])


#cost = np.sqrt(np.sum((mat2-mat)**2))
dist1 = euclidean_distances(mat1)
dist2 = euclidean_distances(mat2)
dist = np.linalg.norm((dist1 - dist2)/2)
print(np.sqrt(np.sum((dist2-dist1)**2)/2))
print((dist2-dist1)**2)
print(np.sqrt(14))
print(dist1)
print(dist2)