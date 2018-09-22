import numpy as np
from dipy.segment.quickbundles import bundles_distances_mdf
from dipy.segment.metric import mdf
from src.tractography.io import read_ply
from src.tractography.viz import draw_brain
from src.tractography.registration import register
from dipy.tracking.streamline import (unlist_streamlines,
                                      center_streamlines,
                                      set_number_of_points,
                                      transform_streamlines)
from dipy.align.streamlinear import compose_matrix44, bundle_min_distance_fast
from dipy.core.optimize import Optimizer
from dipy.core.geometry import compose_transformations
from sklearn.neighbors import KDTree
from scipy.ndimage.interpolation import affine_transform