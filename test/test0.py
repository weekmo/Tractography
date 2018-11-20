import numpy as np
from tractography.Utils import costs
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('fivethirtyeight')

aff = np.load('../dist_only.npy')
print(aff)