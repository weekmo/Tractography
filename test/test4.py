import numpy as np
#from numpy.linalg import eig
from sklearn.decomposition import PCA #,IncrementalPCA
from src.tractography.viz import draw_brain
from src.tractography.io import read_ply
from dipy.align.streamlinear import compose_matrix44
from dipy.tracking.streamline import (transform_streamlines)

#mat = compose_matrix44([0,0,0,0,90,90])
target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
#new_tar = transform_streamlines(target,mat)
#center = np.mean(np.concatenate(target, axis=0), axis=0)

"""
np.random.seed(5)
data = np.array(np.random.randint(10,size=(10,3)))
"""

pca = PCA(n_components=3)
# IncrementalPCA(batch_size=10)
pca.fit(target[0])
#target_T = pca.transform(target[0])
#target_T = pca.fit_transform(target[0])

#pca.fit(new_tar[0])
#new_tar_T = pca.transform(new_tar[0])
#new_tar_T = pca.fit_transform(new_tar[0])

print(pca.components_ )
#draw_brain([[target[0]],[new_tar[0]],[target_T],[new_tar_T]],[[1,0,0],[0,0,1],[.8,0,0],[0,0,.8]])

"""
x = np.random.random((20,3))
val,vec = np.linalg.eig(x)
print(vec)
"""
