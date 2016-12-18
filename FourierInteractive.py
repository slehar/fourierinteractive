# -*- coding: utf-8 -*-
"""
FourInteractive.py

Created on Wed Sep 28 16:36:45 2016

@author: slehar
"""

import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider
from   matplotlib.widgets import CheckButtons
from   PIL import Image
import Tkinter, tkFileDialog
import numpy as np
import numpy.ma as ma
import sys

# Global Variables
rad1 = 0.
rad2 = .15
slidersLocked = False
angle = 0.
angleThresh =  -1.

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
fig.canvas.set_window_title('Fourier Interactive')

# Keypress 'q' to quit callback function
def press(event):
    global ptList, data
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

# Axes for Original Image
axOrig = fig.add_axes([.05, .2, .7/winAspect, .7])
axOrig.axes.set_xticks([])
axOrig.axes.set_yticks([])
axOrig.set_title('Original')

# Read image and display
imgPil = Image.open(imgFile).convert('LA')
imgNp = np.array(imgPil.convert('L'))/255.
ySize, xSize = imgNp.shape
hafY, hafX = int(ySize/2), int(xSize/2)
imgplot = plt.imshow(imgPil, cmap='gray')

# Axes for Fourier Image
axFour = fig.add_axes([.3, .2, .7/winAspect, .7])
axFour.axes.set_xticks([])
axFour.axes.set_yticks([])
axFour.set_title('Fourier')

# Fourier Transform
fourImg  = np.fft.fft2(imgNp)
fourShft = np.fft.fftshift(fourImg)
fourLog  = np.log(np.abs(fourShft))

fourPlot = plt.imshow(fourLog, cmap='gray',
                      vmin=fourLog.min(),
                      vmax=fourLog.max())
plt.pause(.001)

#### Fourier Filtering ####
yy, xx = np.mgrid[-hafY:hafY, -hafX:hafX]
distImg = np.sqrt(xx**2 + yy**2)

angleImg = np.arctan2(yy,xx)
angleImgFlip = np.fliplr(np.flipud(angleImg))

maskImg = (distImg < (rad2 * xSize))
xmask = ma.make_mask(maskImg)
filtImg = fourShft * xmask
filtLog = np.log(np.maximum(np.abs(filtImg),1.))

fourPlot = plt.imshow(filtLog, cmap='gray')
plt.pause(.001)

# Axes for Inverse Fourier Image
axFourInv = fig.add_axes([.56, .2, .7/winAspect, .7])
axFourInv.axes.set_xticks([])
axFourInv.axes.set_yticks([])
axFourInv.set_title('Inverse Fourier')

# Inverse Fourier Transform
fourIshft = np.fft.ifftshift(filtImg)
fourInv   = np.fft.ifft2(fourIshft)
fourReal  = np.real(fourInv)
invPlot = plt.imshow(fourReal, cmap='gray')

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
    plt.sca(axFour)
    maskR1 = (distImg > rad1)
    maskR2 = (distImg < rad2)
    maskRadial = np.logical_and(maskR1, maskR2)
    maskAngle = (np.sin(angleImg*2. + angle) >= angleThresh)          
    maskImg = np.logical_and(maskAngle, maskRadial)  
    maskImg[hafY,hafX] = True
    xmask = ma.make_mask(maskImg)
    filtImg = fourShft * xmask
    filtLog = np.log(np.maximum(np.abs(filtImg),1.))
    fourPlot.set_data(filtLog)
    plt.sca(axFourInv)    
    fourIshft = np.fft.ifftshift(filtImg)
    fourInv  = np.fft.ifft2(fourIshft)
    fourReal = np.real(fourInv)
    invPlot = plt.imshow(fourReal, cmap='gray')       
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
plt.sca(axFour)
#plt.pause(.001)
plt.show()

# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 

