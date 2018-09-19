def export_bundles(bundles, colors=None, show=True, fname=None):
    r""" Visualize and export bundles

    :param bundles: List of numpy.ndarray,
        Bundles to be exported
    :param colors: window.colors
    :param show: Boolean,
        True to show the image(s) or False
    :param fname: str,
        Output file name
    :return:
        Images file(s) and/or show them
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


def draw_brain(bundles_list, colour_list=[]):
    from open3d import LineSet, Vector3dVector, Vector2iVector, draw_geometries
    from random import random
    bundles = []
    for idx, bundle in enumerate(bundles_list):
        if len(colour_list) < 1:
            colour_list = [[random(),random(),random()] for _ in range(len(bundles_list))]
        assert len(bundles_list) == len(colour_list)
        colour = colour_list[idx]
        for points in bundle:
            lines = [[i, i + 1] for i in range(len(points) - 1)]
            data_line = LineSet()
            data_line.points = Vector3dVector(points)
            data_line.lines = Vector2iVector(lines)
            data_line.colors = Vector3dVector([colour for _ in range(len(lines))])
            bundles.append(data_line)
    draw_geometries(bundles)
