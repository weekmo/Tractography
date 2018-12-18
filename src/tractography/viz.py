import numpy as np
from open3d import (LineSet, Vector3dVector, Vector2iVector, draw_geometries,
                    draw_geometries_with_animation_callback)
from random import random


def __rotate_view(vis):
    ctr = vis.get_view_control()
    ctr.rotate(10.0, 0.0)
    return False


def draw_bundles(bundles_list, colour_list=[], rotate=False):
    bundles = []
    for idx, bundle in enumerate(bundles_list):
        if len(colour_list) < 1:
            colour_list = [[random(), random(), random()] for _ in range(len(bundles_list))]
        assert len(bundles_list) == len(colour_list)
        colour = colour_list[idx]
        for points in bundle:
            lines = [[i, i + 1] for i in range(len(points) - 1)]
            data_line = LineSet()
            data_line.points = Vector3dVector(points)
            data_line.lines = Vector2iVector(lines)
            data_line.colors = Vector3dVector([colour for _ in range(len(lines))])
            bundles.append(data_line)
    if rotate:
        draw_geometries_with_animation_callback(bundles, __rotate_view)
    else:
        draw_geometries(bundles)

def clusters_colors(bundle, colours, labels):
    clustered_bundle = []
    counter = 0
    for points in bundle:
        lines = []
        colours_list=[]
        for i,point in enumerate(points):
            if i < (len(points) - 1):
                lines.append([i, i + 1])
                colours_list.append(colours[labels[counter]])
            counter+=1
            #print(idx[counter])
        data_line = LineSet()
        data_line.points = Vector3dVector(points)
        data_line.lines = Vector2iVector(lines)
        data_line.colors = Vector3dVector(colours_list)
        clustered_bundle.append(data_line)
    return clustered_bundle

def lines_colors(bundle, colours, idx):
    coloured_lines = []
    for i in range(len(bundle)):
        lines=[]
        colours_list = []
        for j in range(len(idx[i])-1):
            #print("new colour",j)
            for k in range(idx[i][j],idx[i][j+1]-1):
                lines.append([k,k+1])
                colours_list.append(colours[j])
        data_line = LineSet()
        data_line.points = Vector3dVector(bundle[i])
        data_line.lines = Vector2iVector(lines)
        data_line.colors = Vector3dVector(colours_list)
        coloured_lines.append(data_line)
    return coloured_lines

def draw_clusters(clusters):
    draw_geometries(np.hstack(clusters))