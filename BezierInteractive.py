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
import sys

# Global Variables
freqRad = 0.
freqCirc = 0.
slidersLocked = False
sumVal  = .5
prodVal = .5


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

# Image dimensions
ySize, xSize = (512,512)
hafY, hafX = int(ySize/2), int(xSize/2)


# Axes for  Radial
axRad = fig.add_axes([.1, .2, .5/winAspect, .7])
axRad.axes.set_xticks([])
axRad.axes.set_yticks([])
axRad.set_title('Radial')

# Axes for  Circum
axCir = fig.add_axes([.4, .2, .5/winAspect, .7])
axCir.axes.set_xticks([])
axCir.axes.set_yticks([])
axCir.set_title('Circumf')

# Axes for Mask
axMask = fig.add_axes([.7, .2, .5/winAspect, .7])
axMask.axes.set_xticks([])
axMask.axes.set_yticks([])
axMask.set_title('Mask')


#### Bezier ####
yy, xx = np.mgrid[-hafY:hafY, -hafX:hafX]

distImg = np.sqrt(xx**2 + yy**2)
radialImg = np.sin(distImg/10.)
plt.sca(axRad)
radialPlot = plt.imshow(radialImg, cmap='gray')

angleImg = np.arctan2(yy,xx)
circumImg = np.sin(angleImg*10.)
plt.sca(axCir)
circPlot = plt.imshow(circumImg, cmap='gray')

multImg = (radialImg * circumImg)
sumImg  = (radialImg + circumImg)

plt.sca(axMask)
mergePlot = plt.imshow(multImg, cmap='gray', origin='lower')

# Filter radius sliders
axSlider1 = fig.add_axes([0.3, 0.125, 0.234, 0.04])
axSlider1.set_xticks([])
axSlider1.set_yticks([])

#axSlider2 = plt.axes([0.3, 0.05, 0.237, 0.04])
axSlider2 = fig.add_axes([0.3, 0.05, 0.237, 0.04])
axSlider2.set_xticks([])
axSlider2.set_yticks([])

slider1 = Slider(axSlider1, 'r1', 0.0, 50., valinit=25.)
slider2 = Slider(axSlider2, 'r2', 0.0, 1., valinit=.5)
freqRad, freqCirc = slider1.val, slider2.val

# Filter angular sliders
axSlider3 = fig.add_axes([0.7, 0.125, 0.234, 0.04])
axSlider3.set_xticks([])
axSlider3.set_yticks([])

#axSlider4 = plt.axes([0.7, 0.05, 0.237, 0.04])
axSlider4 = fig.add_axes([0.7, 0.05, 0.237, 0.04])
axSlider4.set_xticks([])
axSlider4.set_yticks([])

slider3 = Slider(axSlider3, 'sum',  0., 1., valinit=.5)
slider4 = Slider(axSlider4, 'product', 0., 1., valinit=.5)
sumVal, prodVal = slider3.val, slider4.val

def update():
    radialImg = np.sin(distImg/freqRad)
    plt.sca(axRad)
    radialPlot.set_data(radialImg)

    circImg = np.sin(angleImg/freqCirc)
    plt.sca(axCir)
    circPlot.set_data(circImg)

    sumImg  = (radialImg + circImg)
    prodImg = (radialImg * circImg)
#    mergeImg = circImg + radialImg
    mergeImg = (sumVal * sumImg) + (prodVal * prodImg)

    plt.sca(axMask)
    mergePlot.set_data(mergeImg)
    plt.pause(.001)

def update1(val):
    global freqRad
    freqRad = slider1.val
    update()

def update2(val):
    global freqCirc
    freqCirc = slider2.val
    update()

def update3(val):
    global sumVal
    sumVal = slider3.val
    update()

def update4(val):
    global prodVal
    prodVal = slider4.val
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
 

