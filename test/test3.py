# Translation Application
# TODO Create ICP Translation class
import numpy as np
from src.tractography.Utils import distance_kdtree
from dipy.align.streamlinear import compose_matrix44
from src.tractography.io import read_ply
from dipy.tracking.streamline import (unlist_streamlines,
                                      center_streamlines,
                                      set_number_of_points,
                                      transform_streamlines)
from dipy.core.optimize import Optimizer
from dipy.core.geometry import compose_transformations
from src.tractography.viz import draw_brain

"""
a = np.array([[1, 2, 0], [5, 6, 4], [7, 3, 8], [9, 12, 19]])
b = a * 2
b = [a, b]
a = [b[0] * 3, b[1] * 3]
"""

target = read_ply('../data/m_ex_atr-left_shore.ply')
subject = read_ply('../data/m_ex_atr-right_shore.ply')
# subject=transform_streamlines(target,compose_matrix44([5,5,5,2,3,4]))

# affine = compose_matrix44([1,1,1])
# y = transform_streamlines(target,affine)

# x = distance_kdtree([1,1,1],moving=target)
# tree = KDTree(target)
# dist, ind = tree.query([[1,2,3],[9,8,7]], k=1)

# print(distance_kdtree([0,0,0],target,y))
# print(target[ind])

a = set_number_of_points(target, 20)
b = set_number_of_points(subject, 20)
a, t_shift = center_streamlines(a)
b, s_shift = center_streamlines(b)
a = np.concatenate(a)
b = np.concatenate(b)
static_mat = compose_matrix44(t_shift)

moving_mat = compose_matrix44(-s_shift)


def dist(x0):
    return distance_kdtree(x0, a, b)


print(distance_kdtree([0, 0, 0], a, b))
options = {'maxcor': 10, 'ftol': 1e-7,
           'gtol': 1e-5, 'eps': 1e-8,
           'maxiter': 100000}
m = Optimizer(dist, [0, 0, 0, 0, 0, 0], method='L-BFGS-B', options=options)

m.print_summary()
mat = compose_matrix44(m.xopt)
mat = compose_transformations(moving_mat, mat, static_mat)
new_subject = transform_streamlines(subject, mat)

# new_subject2 = register(target=target,subject=subject,points=5)[0]

draw_brain([target, subject, new_subject], [[0, 0, 1], [1, 0, 0], [0, 1, 0]])
# draw_brain([target, subject, new_subject,new_subject2], [[0, 0, 1], [1, 0, 0], [.7, 0, 0],[0,1,0]])

"""
b = transform_streamlines(np.array(a), compose_matrix44([1, 2, 3]))
# print(b)
print("------")
# print(a)
dis_mat = bundles_distances_mdf(a, b)
#print(dis_mat)
idx = np.argmin(dis_mat, axis=1)
b = np.array(b)[idx]
a = np.array(a)

print(np.linalg.norm(a[1]-b[1],axis=1))
print(np.sum(np.linalg.norm(a-b,axis=2)))

print(distance_euc([0,0,0],a,b))
"""
"""
print(mdf(a[0], b[0]))
print(mdf(a[0], b[1]))
print(mdf(a[1], b[0]))
print(mdf(a[1], b[1]))
# print(distance([1, 2, 3], target, target))
# print(np.argmin(a, axis=1))
# print(np.min(a, axis=1))
# print(a[[2, 0]])
"""
