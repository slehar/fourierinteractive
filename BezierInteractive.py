# -*- coding: utf-8 -*-
"""
BezierInteractive.py

Created on Mon Dec 19 09:37:14 2016

@author: slehar
"""

import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider
from   matplotlib.widgets import CheckButtons
import numpy as np
import numpy.ma as ma
import sys

# Global Variables
rad1 = 0.
rad2 = .15
slidersLocked = False
angle = 0.
angleThresh =  -1.


# Open figure window
winXSize = 16
winYSize = 6
winAspect = winXSize/winYSize
plt.close('all')
fig = plt.figure(figsize=(winXSize, winYSize))
fig.canvas.set_window_title('Fourier Interactive')

# Keypress 'q' to quit callback function
def press(event):
    sys.stdout.flush()
    if event.key == 'q':
        plt.close()

# Connect keypress event to callback function
fig.canvas.mpl_connect('key_press_event', press)

# Lock Sliders Checkbox
rax = plt.axes([0.2, 0.05, 0.1/winAspect, 0.1])
check = CheckButtons(rax, ['Lock'], [False])

def func(label):
    global slidersLocked
    
    if   label == 'Lock':
        slidersLocked = check.lines[0][0].get_visible()
    plt.draw()
    
check.on_clicked(func)

# Axes for  Image
ySize, xSize = (512,512)
hafY, hafX = int(ySize/2), int(xSize/2)
axOrig = fig.add_axes([.3, .2, .7/winAspect, .7])
axOrig.axes.set_xticks([])
axOrig.axes.set_yticks([])
axOrig.set_title('Bezier')


#### Bezier ####
yy, xx = np.mgrid[-hafY:hafY, -hafX:hafX]
distImg = np.sqrt(xx**2 + yy**2)

angleImg = np.arctan2(yy,xx)
angleImgFlip = np.fliplr(np.flipud(angleImg))

maskImg = (distImg < (rad2 * xSize))
xmask = ma.make_mask(maskImg)

maskPlot = plt.imshow(maskImg, cmap='gray', origin='lower')

# Filter radius sliders
axSlider1 = fig.add_axes([0.3, 0.125, 0.234, 0.04])
axSlider1.set_xticks([])
axSlider1.set_yticks([])

#axSlider2 = plt.axes([0.3, 0.05, 0.237, 0.04])
axSlider2 = fig.add_axes([0.3, 0.05, 0.237, 0.04])
axSlider2.set_xticks([])
axSlider2.set_yticks([])

slider1 = Slider(axSlider1, 'r1', 0.0, xSize, valinit=xSize*rad1)
slider2 = Slider(axSlider2, 'r2', 0.0, xSize, valinit=xSize*rad2)
rad1, rad2 = slider1.val, slider2.val

# Filter angular sliders
axSlider3 = fig.add_axes([0.7, 0.125, 0.234, 0.04])
axSlider3.set_xticks([])
axSlider3.set_yticks([])

#axSlider4 = plt.axes([0.7, 0.05, 0.237, 0.04])
axSlider4 = fig.add_axes([0.7, 0.05, 0.237, 0.04])
axSlider4.set_xticks([])
axSlider4.set_yticks([])

slider3 = Slider(axSlider3, 'angle',  -np.pi, np.pi, valinit=0)
slider4 = Slider(axSlider4, 'thresh', -1., 1., valinit=-1.)
angle, angleThresh = slider3.val, slider4.val

def update():
    global filtImg
    maskR1 = (distImg > rad1)
    maskR2 = (distImg < rad2)
    maskRadial = np.logical_and(maskR1, maskR2)
    maskAngle = (np.sin(angleImg*2. + angle) >= angleThresh)          
    maskImg = np.logical_and(maskAngle, maskRadial)  
    xmask = ma.make_mask(maskImg)
    maskPlot.set_data(xmask)
    plt.pause(.001)

def update1(val):
    global rad1
    rad1 = slider1.val
    update()

def update2(val):
    global rad2
    diff = max((rad2 - rad1), 0.)
    rad2 = slider2.val
    if slidersLocked:
        val1 = rad2 - diff
        slider1.set_val(val1)
    update()

def update3(val):
    global angle
    angle = slider3.val
    update()

def update4(val):
    global angleThresh
    angleThresh = slider4.val
    update()

#    fig.canvas.draw()
slider1.on_changed(update1)
slider2.on_changed(update2)
slider3.on_changed(update3)
slider4.on_changed(update4)

# Show image
plt.ion()
#plt.pause(.001)
plt.show()

# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 

