# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 12:08:15 2017

@author: slehar
"""

import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider
from   matplotlib.widgets import CheckButtons
from   PIL import Image
import Tkinter, tkFileDialog
import numpy as np
import numpy.ma as ma
from scipy.signal import wiener 
#import sys


# Get image using finder dialog
root = Tkinter.Tk()
root.withdraw() # Hide the root window
imgFile = tkFileDialog.askopenfilename(
    initialfile = 'Rover.png')


# Open figure window
winXSize = 16
winYSize = 6
winAspect = winXSize/winYSize
plt.close('all')
fig = plt.figure(figsize=(winXSize, winYSize))
fig.canvas.set_window_title('TestWiener')


# Keypress 'q' to quit callback function
def press(event):
#    sys.stdout.flush()
    if event.key == 'q':
        plt.close()

# Connect keypress event to callback function
fig.canvas.mpl_connect('key_press_event', press)

# Axes for  Radial
axRad = fig.add_axes([.1, .2, .5/winAspect, .7])
axRad.axes.set_xticks([])
axRad.axes.set_yticks([])
axRad.set_title('Radial')

# Axes for  Angular
axAng = fig.add_axes([.4, .2, .5/winAspect, .7])
axAng.axes.set_xticks([])
axAng.axes.set_yticks([])
axAng.set_title('Angular')

# Axes for Mask
axMask = fig.add_axes([.7, .2, .5/winAspect, .7])
axMask.axes.set_xticks([])
axMask.axes.set_yticks([])
axMask.set_title('Mask')


plt.sca(axRad)

# Read image and display
imgPil = Image.open(imgFile).convert('LA')
imgNp = np.array(imgPil.convert('L'))/255.
ySize, xSize = imgNp.shape
hafY, hafX = int(ySize/2), int(xSize/2)
imgplot = plt.imshow(imgPil, cmap='gray')


# slider
axSlider1 = fig.add_axes([0.3, 0.125, 0.234, 0.04])
axSlider1.set_xticks([])
axSlider1.set_yticks([])

slider1 = Slider(axSlider1, 'noise', 0.0, 1., valinit=.5)

noise = slider1.val

wienImg = wiener(imgNp, noise=.1)

plt.sca(axAng)
wienPlot = plt.imshow(wienImg, cmap='gray')

def update1(val):
    global noise
    noise = slider1.val
    wienDat = wiener(imgNp, noise=noise)
    plt.imshow(wienImg, cmap='gray')
    wienPlot.set_data(wienDat)
    plt.pause(.001)

slider1.on_changed(update1)


def update1(val):
    global rad1
    rad1 = slider1.val
    update()








# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 



