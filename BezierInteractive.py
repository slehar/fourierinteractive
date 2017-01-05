# -*- coding: utf-8 -*-
"""
BezierInteractive.py

Not actually a true Bezier curve, this is an interactive exploration
of Radial and Angular periodicity, allowing the radial/angular
frequency to be adjusted by sliders, and the radial and angular images
are combined additively and multiplicatively, also controlled by 
sliders.

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
freqRad = 25.
freqAng = 10.
slidersLocked = False
sumVal  = .5
prodVal = .5

# Open figure window
winXSize = 16
winYSize = 6
winAspect = winXSize/winYSize
plt.close('all')
fig = plt.figure(figsize=(winXSize, winYSize))
fig.canvas.set_window_title('Bezier Interactive')

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


# Axes for  Radial
axRad = fig.add_axes([.1, .2, .5/winAspect, .7])
axRad.axes.set_xticks([])
axRad.axes.set_yticks([])
axRad.set_title('Radial')

# Axes for  Angular
axAng = fig.add_axes([.4, .2, .5/winAspect, .7])
axAng.axes.set_xticks([])
axAng.axes.set_yticks([])
axAng.set_title('Circumf')

# Axes for Mask
axMask = fig.add_axes([.7, .2, .5/winAspect, .7])
axMask.axes.set_xticks([])
axMask.axes.set_yticks([])
axMask.set_title('Mask')


#### Bezier ####
ySize, xSize = (512,512)
hafY, hafX = int(ySize/2), int(xSize/2)
yy, xx = np.mgrid[-hafY:hafY, -hafX:hafX]

# Distance image & radial image
distImg = np.sqrt(xx**2 + yy**2)
distImg = distImg * 2.*np.pi / 512.
radialImg = np.cos(distImg * float(int(freqRad)))
plt.sca(axRad)
radialPlot = plt.imshow(radialImg, cmap='gray')

# Angle image and circumferential image
angleImg = np.arctan2(yy,xx)
circumImg = np.cos(angleImg * float(int(freqAng)))
plt.sca(axAng)
circPlot = plt.imshow(circumImg, cmap='gray')

# Sum and product images
multImg = (radialImg * circumImg)
sumImg  = (radialImg + circumImg)

plt.sca(axMask)
mergePlot = plt.imshow(multImg, cmap='gray', origin='lower')

# Radial frequency slider
axSlider1 = fig.add_axes([0.3, 0.125, 0.234, 0.04])
axSlider1.set_xticks([])
axSlider1.set_yticks([])
slider1 = Slider(axSlider1, 'radial', 0.0, 20., valinit=10.)
freqRad = slider1.val

# Angular frequency slider
axSlider2 = fig.add_axes([0.3, 0.05, 0.237, 0.04])
axSlider2.set_xticks([])
axSlider2.set_yticks([])
slider2 = Slider(axSlider2, 'angular', 0.0, 20., valinit=10.)
freqAng = slider2.val

# Filter angular sliders
axSlider3 = fig.add_axes([0.7, 0.125, 0.234, 0.04])
axSlider3.set_xticks([])
axSlider3.set_yticks([])
slider3 = Slider(axSlider3, 'sum/prod',  0., 1., valinit=.5)
sumProd = slider3.val

axSlider4 = fig.add_axes([0.7, 0.05, 0.237, 0.04])
axSlider4.set_xticks([])
axSlider4.set_yticks([])
slider4 = Slider(axSlider4, 'thresh',    0., 1., valinit=0.)
thresh = slider4.val

def update():
    
    radialImg = np.cos(distImg * float(int(freqRad)))
    plt.sca(axRad)
    radialPlot.set_data(radialImg)

    circImg = np.cos(angleImg * float(int(freqAng)))
    plt.sca(axAng)
    circPlot.set_data(circImg)

    sumImg  = (radialImg + circImg)
    prodImg = (radialImg * circImg)
    mergeImg = (sumVal * sumImg) + (prodVal * prodImg)

    maskImg = (np.fabs(mergeImg) > thresh)
    xmask = ma.make_mask(maskImg)
    filtImg = mergeImg * xmask

    plt.sca(axMask)
    mergePlot.set_data(filtImg)
    plt.pause(.001)

def update1(val):
    global freqRad
    freqRad = slider1.val
    update()

def update2(val):
    global freqAng
    diff = max((freqRad - freqAng), 0.)
    freqAng = slider2.val
    if slidersLocked:
        val1 = freqAng - diff
        slider1.set_val(val1)
    update()

def update3(val):
    global sumVal, prodVal
    sumVal = slider3.val
    prodVal = 1. - sumVal
    update()

def update4(val):
    global thresh
    thresh = slider4.val
    update()

#    fig.canvas.draw()
slider1.on_changed(update1)
slider2.on_changed(update2)
slider3.on_changed(update3)
slider4.on_changed(update4)

# Show image
plt.show()

# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 

