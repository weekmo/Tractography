#!/usr/bin/python3.6
'''
Created on 24 Jul 2018

@author: mohammed
'''


def register(target, subject, points=20):
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
    from dipy.align.streamlinear import StreamlineLinearRegistration
    from dipy.tracking.streamline import set_number_of_points

    cb_subj1 = set_number_of_points(target, points)
    cb_subj2 = set_number_of_points(subject, points)

    srr = StreamlineLinearRegistration()
    srm = srr.optimize(static=cb_subj1, moving=cb_subj2)
    del cb_subj1
    del cb_subj2
    del target
    return srm.transform(subject), srm.matrix


def register_all(data_path):
    r""" Register all ply files in a folder

    :param data_path: str,
        - A folder has subjects each in a folder as ply file format.
        - It will not read ply images putted directly in this folder but inside folders.
        - The subject in the first folder will be targets and the others are moved subjects
    :return: files,
        It wil export aligned subject to trk files each in a new folder as the same name as subject plus _out
    """
    import time
    from os import listdir, mkdir
    from os.path import isfile, isdir
    from tractography.io import read_ply, write_trk, write_ply

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
                aligned_subject = register(target=target, subject=subject)
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


# Done centralise two bundles to origin and return affine matrix
# TODO use PCA to get eigen vectors in each bundle and align them depend on eigen vectors and return affine matrix
# Done knn or kd tree to find the closest point for each point in the target to a point in the subject
# Done calculate the sum of euclidean distances between points in bundles
# from dipy.segment.metric import mdf
# Done minimise the distance by using optimiser and return affine matrix
# TODO create ICP registration function by combining all the above steps