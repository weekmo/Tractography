#!/usr/bin/python3.6
'''
Created on 24 Jul 2018

@author: mohammed
'''

def register(target, subject,points=20):

    r""" Make StreamlineLinearRegistration simpler to use

    Parameters:
    ----------
    :param target: List of numpy.ndarray,
        it is the target bundle witch will be static during registration
    :param subject:List of numpy.ndarray,
        it is the target bundle witch will be moving during registration
    :param points: int,
        The bundles will be divided to this number
    :return: List of numpy.ndarray,
        It the aligned subject to target,
        The function will print out the transformation matrix as well.
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
    print(srm.matrix)
    return srm.transform(subject)

def register_all(data_path):

    r""" Register all ply files in a folder

    :param data_path: str,
        - A folder has subjects each in a folder as ply file format.
        - It will not read ply images putted directly in this folder but inside folders.
        - The subject in the first folder will be targets and the others are moved subjects
    :return: files,
        It wil export aligned subject to trk files each in a new folder as the same name as subject plus _out
    """
    from os import listdir, mkdir
    from os.path import isfile, isdir
    from tractography.io import read_ply,write_trk
    files_names = {}
    index = 0
    target_key = ''
    for dir in listdir(data_path):
        dir = data_path + dir + '/'
        if isdir(dir):
            files_names[dir] = [f for f in listdir(dir) if isfile(dir + f)]

    for k in files_names.keys():
        if index == 0:
            target_key = k
        else:
            output_path = k[:-1] + '_output/'
            if not isdir(output_path):
                mkdir(output_path)
            for target_path, subject_path in zip(files_names[target_key], files_names[k]):
                if target_path == subject_path:
                    target = read_ply(target_key + target_path)
                    subject = read_ply(k + subject_path)
                    aligned_subject = register(target, subject)
                    write_trk(output_path + subject_path, aligned_subject)
        index += 1
        del files_names
