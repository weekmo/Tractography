#!/usr/bin/python3.6
'''
Created on 24 Jul 2018

@author: mohammed
'''
def read_ply(fname):
    """
    Read ply file and return bundles data
    :param fname:
    :return:
    """
    from plyfile import PlyData, PlyElement
    import numpy as np

    ply = PlyData.read(fname)
    data = []
    indeces = np.asarray([i[0] for i in ply.elements[1].data])
    temp = []
    for i, item in enumerate(ply.elements[0].data):
        i += 1
        temp.append([item[3], item[4], item[5]])
        if i in indeces:
            data.append(np.asarray(temp))
            temp = []
    del temp
    del indeces
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
    data_txt = ''
    vert_num = 0
    indeces = []
    index = 0
    with open(fname, 'w') as f:
        for fib in data:
            index += len(fib)
            indeces.append(index)
            for vert in fib:
                data_txt += str(vert[0]) + ' ' + str(vert[1]) + ' ' + str(vert[2]) + '\n'
                vert_num += 1
        f.write('ply\nformat ascii 1.0\n')
        for com in comments:
            f.write('comment ' + com + '\n')
        f.write('element vertices ' + str(vert_num))
        f.write('\nproperty float x\nproperty float y\nproperty float z\n')
        f.write('element fiber {}\nproperty int endindex'.format(len(indeces)))
        f.write('\nend_header\n' + data_txt)
        for i in indeces:
            f.write(str(i) + '\n')

    del data_txt
    del indeces

def write_trk(fname,data):
    """
    Write bundles to trk file format
    :param fname:
    :param data:
    :return:
    """
    import numpy as np
    from dipy.io.streamline import save_trk
    save_trk(fname, streamlines=data, affine=np.eye(4))

def export_bundles(bundles, colors=None, show=True, fname=None):
    """
    Visualize and export bundles
    :param bundles:
    :param colors:
    :param show:
    :param fname:
    :return:
    """
    from dipy.viz import window, actor
    from time import sleep

    ren = window.Renderer()
    ren.SetBackground(1, 1, 1)
    for (i, bundle) in enumerate(bundles):
        color = colors[i]
        lines_actor = actor.streamtube(bundle, color, linewidth=0.3)
        lines_actor.RotateX(-90)
        lines_actor.RotateZ(90)
        ren.add(lines_actor)
    if show:
        window.show(ren)
    if fname is not None:
        sleep(1)
        window.record(ren, n_frames=1, out_path=fname, size=(900, 900))
