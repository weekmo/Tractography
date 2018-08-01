'''
Created on 24 Jul 2018

@author: mohammed
'''


from dipy.align.streamlinear import StreamlineLinearRegistration
from dipy.tracking.streamline import set_number_of_points
from tractographyPly import TractographyPly,show_both_bundles,write_to_file
path1 = '../data/132118/m_ex_atr-left_shore.ply'
path2 = '../data/150019/m_ex_atr-left_shore.ply'
tract1 = TractographyPly(path1)
tract2 = TractographyPly(path2)

cb_subj1 = set_number_of_points(tract1.data, 20)
cb_subj2 = set_number_of_points(tract2.data, 20)

srr = StreamlineLinearRegistration()
srm = srr.optimize(static=cb_subj1, moving=cb_subj2)
cb_subj2_aligned = srm.transform(cb_subj2)


#write_to_file('../data/aligned_atr-left.ply',cb_subj2_aligned,tract2.indeces)
'''
show_both_bundles([cb_subj1, cb_subj2],
                  colors=[window.colors.orange, window.colors.red],
                  show=False,
                  fname='before_registration.png')

show_both_bundles([cb_subj1, cb_subj2_aligned],
                  colors=[window.colors.orange, window.colors.red],
                  show=False,
                  fname='after_registration.png')
'''