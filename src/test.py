'''
Created on 17 Jul 2018

@author: mohammed
'''
from dipy.viz import window, actor
from time import sleep
from dipy.data import two_cingulum_bundles

cb_subj1, cb_subj2 = two_cingulum_bundles()

from dipy.align.streamlinear import StreamlineLinearRegistration
from dipy.tracking.streamline import set_number_of_points