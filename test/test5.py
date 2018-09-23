import numpy as np
from src.tractography.Utils import distance_kdtree
from dipy.align.streamlinear import compose_matrix44
from sklearn.decomposition import PCA
from dipy.core.optimize import Optimizer
from dipy.tracking.streamline import center_streamlines, set_number_of_points, transform_streamlines
from dipy.core.geometry import compose_transformations
from src.tractography.registration import Register_ICP
from src.tractography.io import read_ply
from src.tractography.viz import draw_brain

target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
subject = read_ply('../data/150019/m_ex_atr-left_shore.ply')

options = {'maxcor': 10, 'ftol': 1e-7, 'gtol': 1e-5, 'eps': 1e-8, 'maxiter': 100000}
points = 20


def distance(self, x0):
    return self.distance_kdtree(x0, self.new_static, self.new_moving)


# Centralise two bundles
static = set_number_of_points(target, points)
moving = set_number_of_points(subject, points)

static, s_shift = center_streamlines(static)
moving, m_shift = center_streamlines(moving)

static = np.concatenate(static)
moving = np.concatenate(moving)

# TODO calculate rotation angles
pca = PCA(n_components=3)
static = pca.fit_transform(static)
static_vec = pca.components_

moving = pca.fit_transform(moving)
moving_vec = pca.components_

m = Optimizer(distance, [0, 0, 0, 0, 0, 0], method='L-BFGS-B', options=options)

mat = compose_matrix44(m.xopt)
static_mat = compose_matrix44(s_shift)
moving_mat = compose_matrix44(-m_shift)
mat = compose_transformations(static_mat, mat, moving_mat)
moving = transform_streamlines(moving, mat)
