#!/usr/bin/python3.6
"""
Created on 24 Jul 2018

@author: mohammed
"""


def read_ply(fname, xyz=[3, 4, 5]):
    """
    Read ply file and return bundles data
    :param xyz: array,
        the position of xyz in the file
    :param fname: str,
        File name
    :return:
    """
    from plyfile import PlyData, PlyElement
    import numpy as np

    ply = PlyData.read(fname)
    data = []
    indices = np.asarray([i[0] for i in ply.elements[1].data])
    temp = []
    for i, item in enumerate(ply.elements[0].data):
        i += 1
        temp.append([item[xyz[0]], item[xyz[1]], item[xyz[2]]])
        if i in indices:
            data.append(np.asarray(temp))
            temp = []
    del temp
    del indices
    del ply
    return data

#TODO upload changes to pip
def write_ply(fname, data,
              comments=['DTI Tractography, produced by fiber-track']):
    """
    Write bundles to ply file
    :param fname:
    :param data:
    :param comments:
    :return:
    """
    import numpy as np
    indices_lenghts = np.array([len(i) for i in data])
    with open(fname, 'w') as f:
        f.write('ply\nformat ascii 1.0\n')
        for com in comments:
            f.write('comment ' + com + '\n')
        f.write('element vertices ' + str(sum(indices_lenghts)))
        f.write('\nproperty float x\nproperty float y\nproperty float z\n')
        f.write('element fiber {}\nproperty int endindex'.format(len(indices_lenghts)))
        f.write('\nend_header\n')
        for fib in data:
            for vert in fib:
                f.write(str(vert[0]) + ' ' + str(vert[1]) + ' ' + str(vert[2]) + '\n')
        indices_lenghts = np.cumsum(indices_lenghts)
        for i in indices_lenghts:
            f.write(str(i)+'\n')


def write_trk(fname, data):
    r""" Write bundles to trk file format

    :param fname: str,
        It is the output file name
    :param data: List of numpy.ndarray,
        The bundle to be written
    :return: trk file,
        Export images as trk file format
    """
    import numpy as np
    from dipy.io.streamline import save_trk
    save_trk(fname, streamlines=data, affine=np.eye(4))


def read_trk(fname):
    r""" Read trk file

    :param fname: str,
        The file name to read
    :return: void
    """
    from dipy.io.streamline import load_trk

    return load_trk(fname)[0]
