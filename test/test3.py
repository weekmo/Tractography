# Translation Application
# TODO apply PCA
import numpy as np
from src.tractography.Utils import distance_kdtree, pca_transform
from dipy.align.streamlinear import compose_matrix44
from src.tractography.io import read_ply
from dipy.tracking.streamline import (unlist_streamlines,
                                      center_streamlines,
                                      set_number_of_points,
                                      transform_streamlines)
from dipy.core.optimize import Optimizer
from dipy.core.geometry import compose_transformations
from src.tractography.viz import draw_brain

target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
subject = read_ply('../data/164939/m_ex_atr-left_shore.ply')
# subject=transform_streamlines(target,compose_matrix44([5,5,5,2,3,4]))

subject = pca_transform(target, subject)

a = set_number_of_points(target, 20)
b = set_number_of_points(subject, 20)

a = np.concatenate(a)
b = np.concatenate(b)


def dist(x0):
    return distance_kdtree(x0, a, b)


print(distance_kdtree([0, 0, 0], a, b))
options = {'maxcor': 10, 'ftol': 1e-7,
           'gtol': 1e-5, 'eps': 1e-8,
           'maxiter': 100000}
m = Optimizer(dist, [0, 0, 0, 0, 0, 0], method='L-BFGS-B', options=options)

m.print_summary()
mat = compose_matrix44(m.xopt)
new_subject = transform_streamlines(subject, mat)

draw_brain([target, subject, new_subject], [[0, 0, 1], [1, 0, 0], [.8, 0, 0]])
