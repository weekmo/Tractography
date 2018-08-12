'''
Created on 24 Jul 2018

@author: mohammed
'''
#from dipy.tracking.streamline import transform_streamlines
from tractographyPly import read_ply,write_trk,show_bundles,register # ,register_all
from dipy.viz import window

data1 = read_ply('../data/132118/m_ex_atr-left_shore.ply')
data2 = read_ply('../data/150019/m_ex_atr-left_shore.ply')

# register_all('../data/')
# aligned_bundle=register(traget_path= '../data/132118/m_ex_atr-left_shore.ply',
# subject_path='../data/164939/m_ex_atr-left_shore.ply')
#print(data2)
#aligned_bundle = register(target=data1, subject=data2)
#print(data1)
#write('../data/aligned.ply',aligned_bundle)
write_trk("../data/my_streamlines1.trk", data1)
"""
mat = np.random.rand(4,4)*10
mat[3,0],mat[3,1],mat[3,2],mat[3,3]=0,0,0,1
print("Trans Mat:\n",mat)
test_same_bundle=transform_streamlines(data1,mat)
after = register(target=data1,subject= test_same_bundle)
#write('../data/test.ply',data1)

show_bundles([data1, test_same_bundle],
                  colors=[window.colors.orange, window.colors.blue],
                  show=False,
                  fname='../data/before_registration.png')

show_bundles([data1, after],
                  colors=[window.colors.orange, window.colors.blue],
                  show=False,
                  fname='../data/after_registration.png')
"""