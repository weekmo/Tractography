#!/usr/bin/python3.6
'''
Created on 24 Jul 2018

@author: mohammed
'''


def fake_registration():
    import numpy as np
    from dipy.tracking.streamline import transform_streamlines
    from src.tractography.io import read_ply
    from src.tractography.registration import register
    from src.tractography.viz import draw_brain

    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')

    '''Fake registration'''
    '''Around X axis'''
    mat = np.eye(4)
    mat[1, 1] = mat[2, 2] = 0
    mat[2, 1] = 1
    mat[1, 2] = -1

    '''Around Y axis'''
    mat1 = np.eye(4)
    mat1[0, 0] = mat[2, 2] = 0
    mat1[0, 2] = 1
    mat1[2, 0] = -1
    '''Around XY axes'''
    mat1 = np.matmul(mat, mat1)

    subject_before_registration = transform_streamlines(target, mat1)
    subject_after_registration, _ = register(target, subject_before_registration)

    '''Move combinations apart'''
    mat2 = np.eye(4)
    mat2[0, 3] = 70

    moved_target = transform_streamlines(target, mat2)
    subject_after_registration = transform_streamlines(subject_after_registration, mat2)

    draw_brain([target, subject_before_registration, moved_target, subject_after_registration],
               [[1, 0, 0], [0, 0, 1], [.7, 0, 0], [0, 0, .7]])


def left_to_right():
    import numpy as np
    from dipy.tracking.streamline import transform_streamlines
    from src.tractography.io import read_ply  # ,write_trk,write_ply
    from src.tractography.registration import register
    from src.tractography.viz import draw_brain

    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    subject = read_ply('../data/132118/m_ex_atr-right_shore.ply')

    subject_after, _ = register(target, subject)

    mat = np.eye(4)
    mat[0, 3] = 100
    moved_target = transform_streamlines(target, mat)
    subject_after = transform_streamlines(subject_after, mat)

    draw_brain([target, subject, moved_target, subject_after],
               [[1, 0, 0], [0, 0, 1], [.7, 0, 0], [0, 0, .7]])


def normal_registration():
    import numpy as np
    from dipy.tracking.streamline import transform_streamlines
    from src.tractography.io import read_ply  # ,write_trk,write_ply
    from src.tractography.registration import register
    from src.tractography.viz import draw_brain

    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    subject = read_ply('../data/150019/m_ex_atr-left_shore.ply')

    subject_after, _ = register(target, subject)

    mat = np.eye(4)
    mat[0, 3] = 70
    moved_target = transform_streamlines(target, mat)
    subject_after = transform_streamlines(subject_after, mat)

    draw_brain([target, subject, moved_target, subject_after],
               [[1, 0, 0], [0, 0, 1], [.7, 0, 0], [0, 0, .7]])

#normal_registration()
#realigne_bundle()
#left_to_right()