#!/usr/bin/python3.6
"""
Created on 24 Jul 2018

@author: mohammed
"""
import numpy as np
from plyfile import PlyData, PlyElement
from dipy.tracking.streamline import unlist_streamlines
from dipy.io.streamline import save_trk,load_trk

def read_ply(fname, xyz=[3, 4, 5]):
    """
    Read ply file and return bundles data
    :param xyz: array,
        the position of xyz in the file
    :param fname: str,
        File name
    :return:
    """

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


def write_ply(fname, data,
              comments=['DTI Tractography, produced by fiber-track']):
    """
    Write bundles to ply file
    :param fname:
    :param data:
    :param comments:
    :return:
    """
    points, idx = unlist_streamlines(data)
    with open(fname, 'w') as f:
        f.write('ply\nformat ascii 1.0\n')
        for com in comments:
            f.write('comment ' + com + '\n')
        f.write('element vertices ' + str(len(points)))
        f.write('\nproperty float x\nproperty float y\nproperty float z\n')
        f.write('element fiber {}\nproperty int endindex'.format(len(idx)))
        f.write('\nend_header\n')
        for vert in points:
            f.write(str(vert[0]) + ' ' + str(vert[1]) + ' ' + str(vert[2]) + '\n')
        for i in idx:
            f.write(str(i) + '\n')


def write_trk(fname, data):
    r""" Write bundles to trk file format

    :param fname: str,
        It is the output file name
    :param data: List of numpy.ndarray,
        The bundle to be written
    :return: trk file,
        Export images as trk file format
    """
    save_trk(fname, streamlines=data, affine=np.eye(4))


def read_trk(fname):
    r""" Read trk file

    :param fname: str,
        The file name to read
    :return: void
    """

    return load_trk(fname)[0]
