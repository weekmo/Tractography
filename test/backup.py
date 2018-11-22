# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 12:53:29 2018

@author: mabdelgadi
"""

def dist_new(x0,static,moving,points,max_dist,lam):
    x0 = np.reshape(x0,(points,7))
    moving = transform(x0,moving)
    
    con_static = np.concatenate(static)
    con_moving = np.concatenate(moving)
    
    '''Distance Cost'''
    dist_cost = kd_tree_cost(con_static,con_moving,max_dist)
    #print("dist",dist_cost)
    
    '''Stiffness Cost'''
    """
    kdtree = KDTree(con_moving)
    idx = kdtree.query_radius(con_moving,r)

    stiff_cost = lam*np.sum([np.sum([np.linalg.norm(con_moving[i] - j) for j in con_moving[idx[i]]]) for i in range(len(con_moving))])
    """
    '''Linkage cost'''
    lnk_cost=link_cost(moving)*lam
    #print("stiff",stiff_cost)
    #costs.append([dist_cost,stiff_cost,lnk_cost])
    costs.append([dist_cost,lnk_cost])
    cost = dist_cost+lnk_cost
    #print(dist_cost,stiff_cost,lnk_cost)
    return cost


v=[]
for i in range(7):
    j = i-2 if i-2>0 else 0
    x = [[j,i],[j+1,i],[j+2,i]]
    [v.append(k) for k in x if k[1]>=k[0] and k[0] <=4]
v=np.array(v)
u = [[1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5]]
u = np.concatenate(u)
D = coo_matrix((u,(v[:,0],v[:,1])),shape=(5,7)).tocsr()

print(D.toarray())

dim = []
for i in range(len_d):
    for j in range(i,i+3):
        dim.append([i,j])