#!/usr/bin/python3.6
'''
Created on 24 Jul 2018

@author: mohammed
'''
import time
import numpy as np
from os import listdir, mkdir
from os.path import isfile, isdir

from dipy.align.streamlinear import StreamlineLinearRegistration, compose_matrix44
from dipy.tracking.streamline import set_number_of_points, transform_streamlines, center_streamlines
from dipy.core.optimize import Optimizer

from .Utils import pca_transform, distance_kdtree
from .io import read_ply, write_trk, write_ply


def register(static, moving, points=20):
    r""" Make StreamlineLinearRegistration simpler to use

    Parameters:
    ----------
    :param target: List of numpy.ndarray,
        it is the target bundle witch will be static during registration
    :param subject:List of numpy.ndarray,
        it is the target bundle witch will be moving during registration
    :param points: int,
        The bundles will be divided to this number
    :return: List of numpy.ndarray, numpy.array
        It return the aligned subject and transformation matrix as well.
    """

    cb_subj1 = set_number_of_points(static, points)
    cb_subj2 = set_number_of_points(moving, points)

    srr = StreamlineLinearRegistration()
    srm = srr.optimize(static=cb_subj1, moving=cb_subj2)
    del cb_subj1
    del cb_subj2
    del static
    return srm.transform(moving), srm.matrix


def register_all(data_path):
    r""" Register all ply files in a folder

    :param data_path: str,
        - A folder has subjects each in a folder as ply file format.
        - It will not read ply images putted directly in this folder but inside folders.
        - The subject in the first folder will be targets and the others are moved subjects
    :return: files,
        It wil export aligned subject to trk files each in a new folder as the same name as subject plus _out
    """

    time_list = {}
    dirs = [dir for dir in listdir(data_path)]
    target_dir = data_path + '/' + dirs[0]
    files = [f for f in listdir(target_dir) if isfile(target_dir + '/' + f) and f.endswith('.ply')]
    for f in files:
        time_list[f] = {}
        start_time = time.clock()
        target = read_ply(target_dir + '/' + f)
        time_list[f]['Loading Target'] = time.clock() - start_time
        for i in range(1, len(dirs)):
            subject_path = data_path + '/' + dirs[i] + '/' + f
            out_path = data_path + '/' + dirs[i] + '/out_' + f
            if isfile(subject_path):
                start_time = time.clock()
                subject = read_ply(subject_path)
                time_list[f]['Loading Subject ' + dirs[i]] = time.clock() - start_time
                start_time = time.clock()
                aligned_subject = register(target, subject)
                time_list[f]['Align Subject ' + dirs[i]] = time.clock() - start_time
                start_time = time.clock()
                write_ply(out_path, aligned_subject)
                write_trk(out_path + '.trk', aligned_subject)
                time_list[f]['Writing ' + dirs[i]] = time.clock() - start_time
    del dirs
    del target_dir
    del files
    del out_path
    del start_time
    del subject_path
    del target
    del subject
    del aligned_subject
    return time_list


def registration_icp(static, moving, points=20, pca=True, maxiter=100000):
    options = {'maxcor': 10, 'ftol': 1e-7,
               'gtol': 1e-5, 'eps': 1e-8,
               'maxiter': maxiter}
    if pca:
        static = pca_transform(static, moving)
    else:
        mean_m = np.mean(np.concatenate(moving), axis=0)
        mean_s = np.mean(np.concatenate(static), axis=0)
        moving = [i - mean_m + mean_s for i in moving]
    original_moving = moving.copy()
    static = set_number_of_points(static, points)
    moving = set_number_of_points(moving, points)

    m = Optimizer(distance_kdtree, [0, 0, 0, 0, 0, 0], args=(static, moving), method='L-BFGS-B',
                  options=options)

    m.print_summary()
    mat = compose_matrix44(m.xopt)
    return transform_streamlines(original_moving,mat)
