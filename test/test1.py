# import time
# import sys
# import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KDTree
# from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA
from src.tractography.io import read_ply
from src.tractography.viz import draw_brain
from src.tractography.Utils import kd_tree_cost, pca_transform_norm
from src.tractography.registration import registration_icp
from open3d import draw_geometries
# from scipy.optimize import minimize

static = read_ply('../data/132118/m_ex_atr-left_shore.ply')
moving = read_ply('../data/150019/m_ex_atr-right_shore.ply')

new_moving = pca_transform_norm(static, moving, 50)
#new_moving2 = registration_icp(static, new_moving,clustering='kmeans',pca=False)


con_static = np.concatenate(static)
con_moving = np.concatenate(moving)
draw_geometries([con_moving])
#con_new_moving = np.concatenate(new_moving)

# con_static = static
# con_moving=moving
kmeans = KMeans(3).fit(con_moving)
idx = {i: np.where(kmeans.labels_ == i)[0] for i in range(3)}
print(idx)
"""
tree = KDTree(con_new_moving)
dist_after_PCA = np.hstack(tree.query(con_static, k=1)[0])


plt.hist(dist_before_PCA,bins='auto')
plt.title("Distance before PCA (Moving is base)")
plt.ylabel("Frequncy")
plt.xlabel("Distance")
plt.savefig('dist_before_PCA2.png', dpi=600)
#plt.show()

plt.hist(dist_after_PCA,bins='auto')
plt.title("Distance After PCA (Moving is base)")
plt.ylabel("Frequncy")
plt.xlabel("Distance")
plt.savefig('dist_after_PCA2.png', dpi=600)
#plt.show()
"""
#draw_brain([static, moving, new_moving], [[1, 0, 0], [0, 0, 1], [0, 1, 0]], rotate=True)
