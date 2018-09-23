import numpy as np
# from numpy.linalg import eig
from sklearn.decomposition import PCA  # ,IncrementalPCA
from src.tractography.viz import draw_brain
from src.tractography.io import read_ply
from dipy.align.streamlinear import compose_matrix44
from dipy.tracking.streamline import (transform_streamlines)

mat = compose_matrix44([20, 20, 20, 90, 90, 90])
target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
new_tar = transform_streamlines(target, mat)
# center = np.mean(np.concatenate(target, axis=0), axis=0)
target = target[0]
subject = new_tar[0]
"""
np.random.seed(5)
data = np.array(np.random.randint(5,size=(5,3)))
"""

pca = PCA(n_components=3)
# IncrementalPCA(batch_size=10)

# target_T = pca.transform(target[0])
# target_T = pca.fit_transform(target[0])

# pca.fit(new_tar[0])
# new_tar_T = pca.transform(new_tar[0])
# new_tar_T = pca.fit_transform(new_tar[0])
# x = pca.fit_transform(target)
# print("-------- Target ---------")
# print(data)
# print("\n-------- X transform ---------")
# print(x)
pca = pca.fit(target)
com = pca.components_
# mean = np.mean(target, axis=0)
# y = target - mean
# y = np.dot(y, pca.components_.T)
print("----------")
pca = pca.fit(subject)
com = np.dot(pca.components_.T, com)
# mean = np.mean(subject,axis=0)/2
# x = y + mean
x = np.dot(target, com)

# print("\n-------- X dot ---------")
# print(y)
draw_brain([[target], [subject], [x]], [[1, 0, 0], [0, 0, 1], [0, 1, 0]])

"""
x = np.random.random((20,3))
val,vec = np.linalg.eig(x)
print(vec)
"""
