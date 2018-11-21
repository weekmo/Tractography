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
