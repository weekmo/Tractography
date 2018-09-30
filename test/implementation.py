#!/usr/bin/python3.6
"""
Created on 24 Jul 2018

@author: mohammed
"""
import numpy as np
from dipy.tracking.streamline import transform_streamlines
from dipy.align.streamlinear import compose_matrix44
from src.tractography.io import read_ply
from src.tractography.registration import register,registration_icp
from src.tractography.viz import draw_brain


def fake_registration():
    mat = compose_matrix44([50, 20, 20, 180, 90, 90])
    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    subject = transform_streamlines(target, mat)

    subject_after_registration, _ = register(target, subject)

    draw_brain([target, subject, subject_after_registration],
               [[1, 0, 0], [0, 0, 1], [0, 0, .7]])


def left_to_right():
    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    subject = read_ply('../data/132118/m_ex_atr-right_shore.ply')

    subject_after, _ = register(target, subject)

    draw_brain([target, subject, subject_after],
               [[1, 0, 0], [0, 0, 1], [0, 0, .7]])


def normal_registration():
    target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
    subject = read_ply('../data/150019/m_ex_atr-left_shore.ply')

    subject_after, _ = register(target, subject)

    draw_brain([target, subject, subject_after],
               [[1, 0, 0], [0, 0, 1], [0, 0, .7]])

def icp_registration():
    target = read_ply('../data/164939/m_ex_atr-left_shore.ply')
    subject = read_ply('../data/150019/m_ex_atr-left_shore.ply')

    subject_T=registration_icp(static=target,moving=subject,pca=False)
    draw_brain([target,subject_T],[[1,0,0],[0,0,1]])

icp_registration()