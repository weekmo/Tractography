import numpy as np
from sklearn.neighbors import KDTree
from sklearn.cluster import KMeans
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import lsqr
#from dipy.tracking.streamline import set_number_of_points
from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles

static = read_ply('data/132118/m_ex_atr-right_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

con_static = np.concatenate(static)
con_moving = np.concatenate(moving)

num = 30
static_clusters = KMeans(n_clusters=num).fit(con_static)
moving_clusters = KMeans(n_clusters=num).fit(con_moving)

static_centers = static_clusters.cluster_centers_
moving_centers = moving_clusters.cluster_centers_

kdtree = KDTree(moving_centers)
distances,ids = kdtree.query(con_moving,k=num)
distances[distances==0]=1 #centroid distance must be 1
distances=1/distances  #heigh value for close verteces
# distances = np.divide(distances,distances.sum(axis=1).reshape((distances.shape[0],1)))
weights = distances[:,0]/distances.sum(axis=1) #The weigh is 


new_moving_centers = np.ones((num,4))
new_moving_centers[:,:-1] = static_centers

D = coo_matrix((np.concatenate(new_moving_centers),
                (np.repeat(np.arange(num),4),np.arange(num*4))),
                (num,num*4)).tocsr()

WD = np.dot(weights,D)


tract = np.array([lsqr(WD,moving_centers[:,0])[0],
                   lsqr(WD,moving_centers[:,1])[0],
                   lsqr(WD,moving_centers[:,2])[0]]).T


result = D.dot(tract)



