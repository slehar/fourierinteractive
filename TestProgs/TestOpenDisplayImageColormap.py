# -*- coding: utf-8 -*-
"""
TestOpenDisplayImageColormap.py

Created on Wed Sep 28 16:36:45 2016

@author: slehar
"""

import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider
import Tkinter, tkFileDialog
from   PIL import Image
import matplotlib.image as mpimg
import numpy as np
import sys


# Read in image1 with Tkinter file dialog
root = Tkinter.Tk()
root.withdraw()
imgFile = tkFileDialog.askopenfilename(
    title = 'Select image',
    initialfile = 'Rover.png')
print 'imgFile = %r'%imgFile

img1 = mpimg.imread(imgFile)


imgPil = Image.open(imgFile).convert('LA')
imgNp = np.array(imgPil.convert('L'))/255.
ySize, xSize = imgNp.shape
hafY, hafX = int(ySize/2), int(xSize/2)
imgplot = plt.imshow(imgPil, cmap='gray')


#img1 /= img1.max()
#print 'shape (%d, %d)'%(img1.shape[0], img1.shape[1])


# Generate ramp image
def ramp(y, x):
    return x
img2 = np.fromfunction(ramp,(128,128))
img2 /= img2.max()

# Open figure window
winXSize = 6
winYSize = 6
plt.close('all')
fig = plt.figure(figsize=(winXSize, winYSize))
ax1  = fig.add_axes([.1, .2,  .4, .7])
ax1.set_xticks([]); ax1.set_yticks([])
ax2  = fig.add_axes([.6, .2,  .3, .7])
ax2.set_xticks([]); ax2.set_yticks([])
ax3  = fig.add_axes([.1, .05, .8, .1])
ax3.set_xticks([]); ax3.set_yticks([])

# Keypress 'q' to quit callback function
def press(event):
    global ptList, data
    sys.stdout.flush()
    if event.key == 'q':
        plt.close()

# Connect keypress event to callback function
fig.canvas.mpl_connect('key_press_event', press)

plt.sca(ax1)
imgplot = plt.imshow(img1, cmap='gray')

plt.sca(ax2)
imgplot = plt.imshow(img2, cmap='gray')

slider1 = Slider(ax3, 'colormap', 0.0, 1.0, valinit=.5)

def update(val):
    plt.sca(ax1)
    plt.clim(0., val)
    plt.sca(ax2)
    plt.clim(0., val)
#    fig.canvas.draw()
    plt.pause(.001)
    
slider1.on_changed(update)

#plt.sca(ax1)
plt.ion()
plt.show()

# Pop window to top upper-left
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 

