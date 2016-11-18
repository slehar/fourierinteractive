# -*- coding: utf-8 -*-
"""
TestOpenDisplayImageColormap.py

Created on Wed Sep 28 16:36:45 2016

@author: slehar
"""

import Tkinter, tkFileDialog
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider
#import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap


global vmin, vmax

# Linear Segmented Colormap
cdictGray = {'red':   ((0.0, 0.0, 1.0),
                       (1.0, 1.0, 1.0)),
             'green': ((0.0, 0.0, 1.0),
                       (1.0, 1.0, 1.0)),
             'blue':  ((0.0, 0.0, 1.0),
                       (1.0, 1.0, 1.0))}

colors = np.arange(0., 1., 1./256.)
mygraymap = LinearSegmentedColormap.from_list('graymap', [[v,v,v] for v in colors])
#plt.set_cmap(mygraymap)
plt.set_cmap('gray')

root = Tkinter.Tk()
#root.Font(family="Times", size=10, weight=tkFont.BOLD)
root.withdraw()

imgFile = tkFileDialog.askopenfilename(
    title = 'Select image',
    initialfile = 'Rover.png')

# Open figure window
winXSize = 6
winYSize = 6
plt.close('all')
fig = plt.figure(figsize=(winXSize, winYSize))
ax  = fig.add_axes([.1,.2,.8,.7])
ax1 = fig.add_axes([.1,.05,.8,.1])
ax1.set_xticks([])
ax1.set_yticks([])

# Keypress 'q' to quit callback function
def press(event):
    global ptList, data
    sys.stdout.flush()
    if event.key == 'q':
        plt.close()

# Connect keypress event to callback function
fig.canvas.mpl_connect('key_press_event', press)

img = mpimg.imread(imgFile)
(vmin, vmax) = (img.min(), img.max())
plt.sca(ax)
imgplot = plt.imshow(img, vmin=vmin, vmax=vmax)
imgplot.axes.set_xticks([])
imgplot.axes.set_yticks([])

slider1 = Slider(ax1, 'colormap', 0.0, 1.0, valinit=.5)

def update(val):
    global vmin, vmax
#    print 'update %5.2f'%val
    print 'update %5.2f'%imgplot.get_clim()[1]
    plt.sca(ax)
    imgplot.set_clim(0., val)
#    cdictGray = {'red':   ((0.0, 0.0, val),
#                           (1.0, 1.0, val)),
#                 'green': ((0.0, 0.0, val),
#                           (1.0, 1.0, val)),
#                 'blue':  ((0.0, 0.0, val),
#                           (1.0, 1.0, val))}
#    
#    colors = np.arange(0., val, 1./256.)
#    mygraymap = LinearSegmentedColormap.from_list('graymap', [[v,v,v] for v in colors])

#    newmap = LinearSegmentedColormap.from_list(
#        'graymap', cdictGray)

#    plt.set_cmap(mygraymap)
#    imgplot.draw()
    plt.pause(.001)
#    fig.canvas.draw()
    
slider1.on_changed(update)

plt.sca(ax)
plt.ion()
plt.show()


figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 

