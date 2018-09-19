import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from src.tractography.viz import draw_brain
from src.tractography.io import read_ply, write_ply
from dipy.tracking.streamline import (unlist_streamlines,
                                      center_streamlines,
                                      set_number_of_points)

target = read_ply('../data/132118/m_ex_atr-left_shore.ply')
source = read_ply('../data/150019/m_ex_atr-left_shore.ply')
new_target = set_number_of_points(target, 20)
new_source = set_number_of_points(source, 20)
centerd_source, shift1 = center_streamlines(new_source)
centerd_target, shift2 = center_streamlines(new_target)
# x,y = unlist_streamlines(target)
# print(centerd)
# draw_brain([centerd_source,centerd_target])
primary = centerd_target[0]
secondary = centerd_source[0]


n = primary.shape[0]

pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
unpad = lambda x: x[:,:-1]
X = pad(primary)
Y = pad(secondary)

# Solve the least squares problem X * A = Y
# to find our transformation matrix A
A, res, rank, s = np.linalg.lstsq(X, Y)
transform = lambda x: unpad(np.dot(pad(x), A))
'''
def dist(x):
    return np.linalg.norm(x[0] - x[1], axis=1)


# m = cost(primary,secondary)
# m = dist([primary,secondary])
m = minimize(dist, [primary, secondary], method='Powell')
#m = minimize(dist, [primary, secondary], maxiter=2000, full_output=True, method='Powell', args=(0.1, 0.2))
# p = lambda x: np.hsplit(x,2)
print(m.x)

fig = plt.figure(figsize=(5,4),dpi=80)
plt.plot(y,np.hsplit(primary,3)[2])
plt.show()
'''
# print(p,primary)
draw_brain([[transform(secondary)],[primary],[secondary]],[[1,0,0],[0,0,1],[.8,0,0]])
