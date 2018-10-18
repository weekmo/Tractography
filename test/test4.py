import numpy as np
# from numpy.linalg import eig
# from  nibabel.streamlines.tck import TckFile
from sklearn.decomposition import PCA
from src.tractography.viz import draw_brain
from src.tractography.io import read_ply, write_trk, write_ply
from dipy.align.streamlinear import compose_matrix44
from dipy.tracking.streamline import (unlist_streamlines,
                                      center_streamlines,
                                      set_number_of_points,
                                      transform_streamlines)
from time import time
from src.tractography.registration import registration_icp


def original_transform():
    mat = compose_matrix44([20, 20, 20, 180, 90, 90])
    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    subject = read_ply('../data/150019/m_ex_atr-left_shore.ply')

    # Move and rotate the subject
    subject = transform_streamlines(subject, mat)

    # Reduce # of points
    # target_T = set_number_of_points(target, 20)
    subject_T = set_number_of_points(subject, 20)

    # Concatenate bundles to calculate
    # singular vectors and mid point
    con_target = np.concatenate(target)
    con_subject = np.concatenate(subject)

    # Move the subject to the origin
    mean = np.mean(con_subject, axis=0)
    subject_T = subject_T - mean

    # Move the subject to the target
    mean = np.mean(con_target, axis=0)
    subject_T = subject_T + mean

    pca = PCA(n_components=3)

    pca = pca.fit(con_subject)
    print(pca.components_)
    subject_T = np.dot(subject_T, pca.components_.T)

    pca = pca.fit(con_target)
    print(pca.components_)
    subject_T = np.dot(subject_T, pca.components_.T)

    draw_brain([target, subject, subject_T],
               [[0, 0, 1], [1, 0, 0], [.7, 0, 0]])


def dot_transformation():
    # mat = compose_matrix44([0, 0, 0, 90, 90, 90])
    mat = compose_matrix44([50, 20, 20, 180, 90, 90])
    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    # subject = read_ply('../data/164939/m_ex_atr-left_shore.ply')

    subject = transform_streamlines(target, mat)

    # target_T = set_number_of_points(target, 20)
    subject_T = set_number_of_points(subject, 20)
    # subject_T = subject

    con_target = np.concatenate(target)
    con_subject = np.concatenate(subject)

    pca = PCA(n_components=3)

    pca = pca.fit(con_subject)
    mean = np.mean(con_subject, axis=0)
    subject_T = subject_T - mean
    subject_T = np.dot(subject_T, pca.components_.T)
    # print(pca.components_.T)

    pca = pca.fit(con_target)
    # vec = np.linalg.inv(pca.components_.T)
    subject_T = np.dot(subject_T, pca.components_)
    mean = np.mean(con_target, axis=0)
    subject_T = subject_T + mean
    print("Normal\n", pca.components_)
    print("\nTranspose\n", pca.components_.T)
    # print("\nInvert\n",vec)

    """
    write_trk('../data/target_T.trk',target_T)
    write_trk('../data/subject_T.trk', subject_T)

    write_ply('../data/target_T.ply', target_T)
    write_ply('../data/subject_T.ply', subject_T)
    """
    draw_brain([target, subject, subject_T],
               [[1, 0, 0], [0, 0, 1], [0, 0, .8]])


# dot_transformation()

def new_pca():
    mat = compose_matrix44([50, 20, 20, 180, 90, 90])
    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    # subject = read_ply('../data/164939/m_ex_atr-left_shore.ply')

    subject = transform_streamlines(target, mat)
    start = time()
    con_target = np.concatenate(target)
    con_subject = np.concatenate(subject)

    pca = PCA(n_components=3)

    pca = pca.fit(con_subject)
    mat1 = pca.components_.T

    pca = pca.fit(con_target)
    mat2 = pca.components_

    aff = np.dot(mat1, mat2)
    subject_T = [np.dot(i, aff) for i in subject]

    center3 = np.mean(con_target, axis=0) - np.mean(np.concatenate(subject_T), axis=0)
    subject_T = [s + center3 for s in subject_T]
    print(time() - start)
    # draw_brain([target, subject,subject_T],
    #           [[1, 0, 0], [0, 0, 1], [0, 0, .8]])


def new_pca2():
    mat = compose_matrix44([50, 20, 20, 180, 90, 90])
    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    subject = read_ply('../data/197348/m_ex_atr-left_shore.ply')

    # subject = transform_streamlines(target, mat)
    start = time()
    con_target = np.concatenate(target)
    con_subject = np.concatenate(subject)

    pca = PCA(n_components=3)

    pca = pca.fit(con_subject)
    mat1 = pca.components_.T

    pca = pca.fit(con_target)
    mat2 = pca.components_

    aff = np.dot(mat1, mat2)

    mean_s = np.mean(con_subject, axis=0)
    mean_t = np.mean(con_target, axis=0)
    subject_T = [np.dot((i - mean_s), aff) + mean_t for i in subject]

    print(time() - start)
    draw_brain([target, subject, subject_T],
               [[1, 0, 0], [0, 0, 1], [0, 0, .8]])


# new_pca()
# new_pca2()
def test_pca():
    # mat = compose_matrix44([50, 20, 20])
    target = read_ply('../data/164939/m_ex_atr-left_shore.ply')
    subject = read_ply('../data/150019/m_ex_atr-left_shore.ply')

    # subject = transform_streamlines(target, mat)
    # subject_T=registration_icp(static=target,moving=subject,pca=False)
    draw_brain([target, subject])
    # print(len(subject_T))
    # register1 = Registration(static=target,moving=subject)
    # subject_T = register1.optimize(pca=False)
    # mean_m = np.mean(np.concatenate(subject),axis=0)
    # mean_s = np.mean(np.concatenate(target),axis=0)
    # subject_T=[i-mean_m+mean_s for i in subject]

    # subject_R,_ = register(target,subject)
    # draw_brain([target, subject,subject_T,subject_R],
    #           [[1, 0, 0], [0, 0, 1], [1, 1, 0],[1,1,0]])
    # draw_brain([target, subject,subject_T],[[1, .7, .7], [0, 0, 1], [1,0 , 0]])


test_pca()
"""
def rdm_data_test():
    np.random.seed(5)
    x = np.random.random((5, 3))
    y = np.random.random((5, 3))

    print(x, '\n ------ \n', y)
    print('\n ------ \n')
    pca = PCA(n_components=3)

    pca = pca.fit(x)
    mat1 = pca.components_.T
    mean = np.mean(x, axis=0)
    xt = x - mean
    xt = np.dot(xt, mat1)

    pca = pca.fit(y)
    mean = np.mean(y, axis=0)
    yt = y - mean
    yt = np.dot(y, pca.components_.T)

    print(xt, '\n --------- \n', yt)
    draw_brain([[x], [y], [xt], [yt]], [[1, 0, 0], [0, 1, 0], [.8, 0, 0], [0, .7, 0]])
    # draw_brain([[x], [yt]],[[1, 0, 0], [0, 1, 0]])


def angles():
    x = np.array([[0, 0, 0], [3, 0, 0]])
    y = np.array([[0, 0, 0], [0, 3, 0]])
    mat = np.array([[4581, 0, .894], [0, 1, 0], [-.894, 0, .4581]])
    yt = np.dot(y, mat.T)
    print(yt)
    # draw_brain([[x],[y],[yt]],
    #          [[1,0,0],[0,1,0],[0,.8,0]])


def dot_trans2():
    mat = compose_matrix44([0, 0, 0, 90, 90, 90])
    target = read_ply('../data/m_ex_atr-left_shore.ply')
    subject = transform_streamlines(target, mat)

    target = target[0]
    subject = subject[0]

    pca = PCA(n_components=3)

    pca = pca.fit(target)
    mean = np.mean(subject, axis=0)
    subject_T = subject - mean
    subject_T = np.dot(subject_T, pca.components_.T)
    print(subject_T)

    # draw_brain([[target], [subject], [subject_T]],[[1, 0, 0], [0, 0, 1], [0, 0, .8]])

def curve():
    #np.random.seed(10)
    zeros = np.zeros((50,1))
    range = np.arange(0,50).reshape(50,1)
    xaxis = np.hstack((range,zeros,zeros))
    yaxis = np.hstack((zeros,range,zeros))
    zaxis = np.hstack(( zeros, zeros,range))
    z = np.ones((300,1))
    x = np.linspace(0,50,300).reshape((300,1))
    y = np.sin(x)
    #print(x.shape,z.shape,y.shape)
    result = np.hstack((x,y,z))
    #print(zaxis)
    draw_brain([[result],[xaxis],[yaxis],[zaxis]])

x = np.random.random((20,3))
val,vec = np.linalg.eig(x)
print(vec)
"""
