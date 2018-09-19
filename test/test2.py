import numpy as np
from dipy.tracking.streamline import transform_streamlines
from src.tractography.viz import draw_brain
from scipy.optimize import minimize
"""
primary = np.array([[40., 1160., 0.],
                    [40., 40., 0.],
                    [260., 40., 0.],
                    [260., 1160., 0.]])

secondary = np.array([[610., 560., 0.],
                      [610., -560., 0.],
                      [390., -560., 0.],
                      [390., 560., 0.]])
#primary = np.hstack([primary,np.ones((primary.shape[0],1))])

x = np.array([[1,2,3],
              [4,5,6],
              [7,8,9],
              [10,11,12],
              [13,14,15],
              [16,17,18]])
#x =np.hstack([x,np.ones((x.shape[0],1))])
print(x)
A = np.eye(4)
A[0,3] = 1
print(transform_streamlines([x],A))
"""
x = np.array([[1,2,3],
              [4,5,6],
              [7,8,9],
              [10,11,12],
              [13,14,15],
              [16,17,18]])
y=x*2
print(y)
#draw_brain([[x],[y]])

def cost(x,y):
    return np.sqrt(np.sum([(x[0]-y[0])**2,(x[1]-y[1])**2,(x[2]-y[2])**2]))


m = minimize(cost,x,args=y,method = 'Powell')
z=m.x.reshape((x.shape[0],3))
print(z)
draw_brain([[x],[y],[z]],[[1,0,0],[0,0,1],[.8,0,0]])
#print(m.fun)
#print(cost(x,y))
