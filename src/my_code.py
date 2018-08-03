'''
Created on 24 Jul 2018

@author: mohammed
'''

from shutil import copyfile
from dipy.align.streamlinear import StreamlineLinearRegistration
#from streamlinear import StreamlineLinearRegistration
from dipy.tracking.streamline import set_number_of_points
from dipy.viz import window
from tractographyPly import TractographyPly,show_both_bundles,write_to_file
def register(traget_path,subject_path,points=40):
    tract1 = TractographyPly(traget_path)
    tract2 = TractographyPly(subject_path)

    cb_subj1 = set_number_of_points(tract1.data, points)
    cb_subj2 = set_number_of_points(tract2.data, points)

    srr = StreamlineLinearRegistration()
    srm = srr.optimize(static=cb_subj1, moving=cb_subj2)
    #print(srm.matrix)
    return srm.transform(tract2.data)
"""
copyfile(path1,data_path+'subject_target.ply')
copyfile(path2,data_path+'subject_before.ply')
write_to_file('../data/subject_after.ply',cb_subj2_aligned)

show_both_bundles([tract1.data, tract2.data],
                  colors=[window.colors.orange, window.colors.red],
                  show=False,
                  fname='../data/before_registration.png')

show_both_bundles([tract2.data, cb_subj2_aligned],
                  colors=[window.colors.orange, window.colors.red],
                  show=False,
                  fname='../data/after_registration.png')
"""