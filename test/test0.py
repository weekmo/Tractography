import numpy as np
from tractography.Utils import costs
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('fivethirtyeight')

'''
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(x):
    from tractography.Utils import costs
    ax1.clear()
    ax1.plot(costs)
    
    plt.title('Cost Function')
    plt.legend(['Distance','Stiffnes'])

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
'''