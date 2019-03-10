import numpy as np

from scipy import sparse
from scipy.sparse.linalg import lsqr
#from dipy.tracking.streamline import set_number_of_points
from dipy.align.streamlinear import compose_matrix44

from time import time

import matplotlib.pyplot as plt

from src.tractography.io import read_ply
from src.tractography.registration import register
from src.tractography.viz import draw_bundles

moving = read_ply('data/197348/m_ex_atr-right_shore.ply')
con_moving = np.concatenate(moving)
length = con_moving.shape[0]

affine1 = np.array([compose_matrix44([0,0,0, i/1000,i/1000,0])[:3,:].T for i in range(length)])
affine2 = np.vstack(affine1)
#affine1 = np.concatenate(affine1)

new_con_moving = np.ones((length,4))
new_con_moving[:,:-1] = con_moving

D = sparse.coo_matrix((np.concatenate(new_con_moving),
                (np.repeat(np.arange(length),4),np.arange(length*4))),
                (length,length*4)).tocsr()

new_con_mov = D.dot(affine2)

i = 0
end=0
new_moving=[]
for track in moving:
    end = len(track)+i
    new_moving.append(new_con_mov[i:end])
    #new_moving.append([i,end])
    i = end


#draw_bundles([new_moving,moving],[[0,0,1],[1,0,0]])



''' ICP '''
static = moving
moving = new_moving
#draw_bundles([moving,static],[[0,0,1],[1,0,0]])


''' Get points cloud '''
con_static = np.concatenate(static)
con_moving = np.concatenate(moving)
print(np.count_nonzero(con_moving))


distances = np.linalg.norm(con_static-con_moving,axis=1)

''' Get the threshold '''
max_range = max(distances)
plt.hist(distances, bins='auto',range=(0,max_range))
#plt.title("Original Position\nTotal distance: {:}".format(round(distances.sum(),2)))
plt.ylabel("Frequency")
plt.xlabel("Distance")
plt.savefig('new_plan/1{:02d}_hist_original.png'.format(num), dpi=600)

length = len(con_moving)
threshold=20
alpha = 9999
lamb = 1

W = np.where(distances>threshold,0,1)
count = np.unique(W,return_counts=True)

''' Make w diagonal '''
W = sparse.diags(W)


# W = sparse.diags(np.where(dist<threshold,0,1))
# I = sparse.identity(3)
# K = sparse.kron(W,I)
''' Moving in homogeneouse coordinates '''
new_con_moving = np.ones((length,4))
new_con_moving[:,:-1] = con_moving

D = sparse.coo_matrix((np.concatenate(new_con_moving),
                (np.repeat(np.arange(length),4),np.arange(length*4))),
                (length,length*4)).tocsr()
''' Get WD '''
WD = W.dot(D)
''' Get U '''
# U = con_static[ids]
''' Get WD '''
WU = W.dot(con_static)

''' Stiffnes '''
length = con_moving.shape[0]-len(moving)
data = np.tile([-1,1],length)
row = np.arange(length).repeat(2)

col=[]
j=0
for track in moving:
    end = j+track.shape[0]
    col.append(np.arange(j,end).repeat(2)[1:-1])
    j = end
col = np.concatenate(col)

M = sparse.csr_matrix((data,(row,col)),(length,con_moving.shape[0]))

''' Get G '''
# G = sparse.diags([1,1,1,lamb])
MG = alpha*sparse.kron(M,sparse.diags([1,1,1,lamb])).tocsr()
''' Get Zeros '''
zer = np.zeros((MG.shape[0],3))

A = sparse.vstack([MG,WD])
B = np.vstack([zer,WU])

X = np.zeros((A.shape[1],3))
acon = np.zeros((3))

start = time()
for i in range(3):
    result = np.array(lsqr(A,B[:,i]))
    X[:,i] = result[0]
    acon[i] = result[6]
    print(result[1:-1])
end = time()
print(np.average(acon))

'''    
X = np.array([lsqr(A,B[:,0])[0,6],lsqr(A,B[:,1])[0,6],lsqr(A,B[:,2])[0,6]]).T
'''

np.save('new_plan/1{:02d}_x.npy'.format(num),X)

hours   = int(( end - start)/3600)
minutes = int(((end - start)%3600)/60)
seconds = int(((end - start)%3600)%60)
print("Duration: {:02}:{}:{}".format(hours,minutes,seconds))

new_con_mov=D.dot(X)

i = 0
end=0
new_moving=[]
for track in moving:
    end = len(track)+i
    new_moving.append(new_con_mov[i:end])
    #new_moving.append([i,end])
    i = end
    
# bins='auto'
''' Get the threshold '''
distances = np.linalg.norm(con_static-new_con_mov,axis=1)
plt.hist(distances, bins='auto')
#plt.title("After ICP | Duration: {:02}:{:02}:{:02}, Total Distance: {:}"
#          .format(hours,minutes,seconds,round(distances.sum(),2))+
#          "\nMax distance: "+str(threshold)+"mm, alpha: "+str(alpha))
plt.ylabel("Frequency")
plt.xlabel("Distance")
plt.savefig('new_plan/1{:02d}_hist_ICP.png'.format(num), dpi=600)

draw_bundles([new_moving,static],[[0,0,1],[1,0,0]])

dipy_moving = register(moving,new_moving)
draw_bundles([dipy_moving,moving],[[0,0,1],[1,0,0]])




'''Dipy'''
''' Plot the distance '''
distances = np.linalg.norm(con_moving-np.concatenate(dipy_moving),axis=1)
plt.hist(distances, bins='auto')
#plt.title("dypi | Duration: {:02}:{:02}:{:02}, Total Distance: {:}"
#          .format(hours,minutes,seconds,round(distances.sum(),2))+
#          "\nMax distance: "+str(threshold)+"mm, alpha: "+str(alpha))
plt.ylabel("Frequency")
plt.xlabel("Distance")
plt.savefig('new_plan/1{:02d}_hist_dipy.png'.format(num), dpi=600)