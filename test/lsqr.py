import numpy as np

from sklearn.neighbors import KDTree
from sklearn.cluster import KMeans

from scipy.sparse import coo_matrix
from scipy.sparse.linalg import lsqr

from nibabel.affines import apply_affine
#from dipy.tracking.streamline import set_number_of_points
from dipy.align.streamlinear import compose_matrix44

from src.tractography.io import read_ply
from src.tractography.viz import draw_bundles

static = read_ply('data/132118/m_ex_atr-right_shore.ply')
moving = read_ply('data/150019/m_ex_atr-right_shore.ply')

''' Get points cloud '''
con_static = np.concatenate(static)
con_moving = np.concatenate(moving)

num = 5
static_clusters = KMeans(n_clusters=num).fit(con_static)
moving_clusters = KMeans(n_clusters=num).fit(con_moving)

static_centers = static_clusters.cluster_centers_
moving_centers = moving_clusters.cluster_centers_

''' I've tried this as stiffness:
Ax = b - dist
'''
kdtree = KDTree(moving_centers)
dist = kdtree.query(moving_centers,k=num)[0].sum(axis=1).reshape((num,1))

new_moving_centers = np.ones((num,4))
new_moving_centers[:,:-1] = moving_centers

D = coo_matrix((np.concatenate(new_moving_centers),
                (np.repeat(np.arange(num),4),np.arange(num*4))),
                (num,num*4)).tocsr()

new_static_centers = static_centers-dist
x = np.array([lsqr(D,new_static_centers[:,0])[0],
                   lsqr(D,new_static_centers[:,1])[0],
                   lsqr(D,new_static_centers[:,2])[0]]).T

''' I get the same new_static_centers '''
print(D.dot(x))

''' Apply soft membership'''
def transform(affine,bundle,clusters_centers):
    num = len(clusters_centers)
    kdtree = KDTree(clusters_centers)
    distances,ids = kdtree.query(np.concatenate(bundle),k=num)
    distances[distances==0]=1 #centroid distance must be 1
    distances=1/distances  #heigh value for close verteces
    distances = np.divide(distances,distances.sum(axis=1).reshape((distances.shape[0],1)))
    # weights = distances[:,0]/distances.sum(axis=1) #The weigh is 
    affine  = [compose_matrix44(np.multiply(np.reshape(dis,(num,1)),affine[id]).sum(axis=0)) for dis,id in zip(distances,ids)]
    #Z = [apply_affine(compose_matrix44(np.multiply(np.reshape(dis,(num,1)),x0[id]).sum(axis=0)),vec) for dis,id,vec in zip(distances,ids,con_moving)]
    count = 0
    trans_bundle=[]
    for tract in bundle:
        temp = []
        for vec in tract:
            temp.append(apply_affine(affine[count],vec))
            count+=1
        trans_bundle.append(np.array(temp))
    return trans_bundle

new_moving = transform(x,moving,moving_centers)

draw_bundles([static,moving])