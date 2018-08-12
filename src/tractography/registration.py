'''
Created on 24 Jul 2018

@author: mohammed
'''



def register(target_path=None, subject_path=None, points=20, target=None, subject=None):
    """
    Register bundles
    :param target_path:
    :param subject_path:
    :param points:
    :param target:
    :param subject:
    :return:
    """
    from dipy.align.streamlinear import StreamlineLinearRegistration
    from dipy.tracking.streamline import set_number_of_points

    bundle1 = None
    bundle2 = None

    msq = "Please give a value to one of these parameters, {} " \
          "(file path on your system) or {} (List of bundles)"

    if target is not None:
        bundle1 = target
    elif target_path is not None:
        bundle1 = read(target_path)
    else:
        raise ValueError(msq.format("target_path", "target"))

    if subject is not None:
        bundle2 = subject
    elif subject_path is not None:
        bundle2 = read(subject_path)
    else:
        raise ValueError(msq.format("subject_path", "subject"))

    cb_subj1 = set_number_of_points(bundle1, points)
    cb_subj2 = set_number_of_points(bundle2, points)

    srr = StreamlineLinearRegistration()
    srm = srr.optimize(static=cb_subj1, moving=cb_subj2)
    del cb_subj1
    del cb_subj2
    del bundle1
    print(srm.matrix)
    return srm.transform(bundle2)

def register_all(data_path):
    from os import listdir, mkdir
    from os.path import isfile, isdir

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
                    aligned_subject = register(target_key + target_path, k + subject_path)
                    write(output_path + subject_path, aligned_subject)
        index += 1
        del files_names
