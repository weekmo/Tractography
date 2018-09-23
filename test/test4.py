import numpy as np
# from numpy.linalg import eig
from sklearn.decomposition import PCA  # ,IncrementalPCA
from src.tractography.viz import draw_brain
from src.tractography.io import read_ply
from dipy.align.streamlinear import compose_matrix44
from dipy.tracking.streamline import (transform_streamlines)


def original_transform():
    mat = compose_matrix44([20, 20, 20, 90, 90, 90])
    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    subject = transform_streamlines(target, mat)

    target = target[0]
    subject = subject[0]

    pca = PCA(n_components=3)
    target_T = pca.fit_transform(target)
    subject_T = pca.fit_transform(subject)
    draw_brain([[target], [subject], [target_T], [subject_T]],
               [[1, 0, 0], [0, 0, 1], [.8, 0, 0], [0, 0, .8]])


def dot_transformation():
    mat = compose_matrix44([20, 20, 20, 90, 90, 90])
    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    subject = transform_streamlines(target, mat)

    target = target[0]
    subject = subject[0]

    pca = PCA(n_components=3)

    pca = pca.fit(target)
    mean = np.mean(target, axis=0)
    target_T = target - mean
    target_T = np.dot(target_T, pca.components_.T)

    pca = pca.fit(subject)
    mean = np.mean(subject, axis=0)
    subject_T = subject - mean
    subject_T = np.dot(subject_T, pca.components_.T)

    draw_brain([[target], [subject], [target_T], [subject_T]],
               [[1, 0, 0], [0, 0, 1], [.8, 0, 0], [0, 0, .8]])


def rdm_data_test():
    np.random.seed(10)
    x = np.random.random((5, 3))
    mat = np.array([[1,0,0,5],[0,1,0,5],[0,0,1,5],[0,0,0,1]])
    print(mat)
    return None

    print(x, '\n ------ \n', y)
    pca = PCA(n_components=3)

    pca = pca.fit(x)
    mean = np.mean(x, axis=0)
    x = x - mean
    x = np.dot(x, pca.components_.T)

    pca = pca.fit(y)
    mean = np.mean(y, axis=0)
    y = y - mean
    y = np.dot(y, pca.components_.T)

    print(x, '\n --------- \n', y)
    draw_brain([[x],[y]],[[1,0,0],[0,0,1]])

rdm_data_test()
"""
x = np.random.random((20,3))
val,vec = np.linalg.eig(x)
print(vec)
"""
