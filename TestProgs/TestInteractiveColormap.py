# -*- coding: utf-8 -*-
"""
TestInteractiveColormap.py

@author: slehar
"""

import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider
import numpy as np

# Open figure window
winXSize = 6
fig = plt.figure()
ax  = fig.add_axes([.1, .2,  .8, .7])
ax.set_xticks([])
ax.set_yticks([])
ax1 = fig.add_axes([.1, .05, .8, .1])
ax1.set_xticks([])
ax1.set_yticks([])

# Generate ramp image
def ramp(y, x):
    return x
img = np.fromfunction(ramp,(128,128))
img /= img.max()

plt.sca(ax)
imgplot = plt.imshow(img, cmap='gray')

slider1 = Slider(ax1, 'colormap', 0.0, 1.0, valinit=.5)

def update(val):
    global vmin, vmax
    plt.clim(0., val)
#    fig.canvas.draw()
#    plt.pause(.001)
    
slider1.on_changed(update)

plt.sca(ax)
plt.ion()
plt.show()

 

