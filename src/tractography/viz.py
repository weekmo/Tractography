from open3d import (LineSet, Vector3dVector, Vector2iVector, draw_geometries,
                    draw_geometries_with_animation_callback)
from random import random


def __rotate_view(vis):
    ctr = vis.get_view_control()
    ctr.rotate(10.0, 0.0)
    return False


def draw_brain(bundles_list, colour_list=[], rotate=False):
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
