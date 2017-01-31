# -*- coding: utf-8 -*-
"""
FourInteractiveHarmonic.py

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
freqRad = 25.
freqAng = 10.
slidersLocked = False
angle = 0.
thresh =  -1.

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
fig.canvas.set_window_title('Fourier Interactive Harmonic')

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

#plt.sca(axFour)
#fourPlot = plt.imshow(fourLog, cmap='gray')
plt.pause(.001)

#### Create Mask ####
yy, xx = np.mgrid[-hafY:hafY, -hafX:hafX]

# Dist image and radial sinusoid
distImg  = np.sqrt(xx**2 + yy**2)
distImg = distImg * 2. * np.pi / float(xSize)
radialImg = np.cos(distImg  * float(int(freqRad )))

# Angle image and circumferential sinusoid
angleImg = np.arctan2(yy,xx)
circumImg   = np.cos((angleImg + angle) * float(int(freqAng)))

mergeImg  = radialImg * circumImg
maskImg   = (mergeImg > thresh)
xmask   = ma.make_mask(maskImg)
filtImg = fourShft * xmask
filtLog = np.log(np.maximum(np.abs(filtImg),1.))
plt.sca(axFour)
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
plt.sca(axFourInv)
invPlot = plt.imshow(fourReal, cmap='gray')

# Filter radius sliders
axSlider1 = fig.add_axes([0.3, 0.125, 0.234, 0.04])
axSlider1.set_xticks([])
axSlider1.set_yticks([])

#axSlider2 = plt.axes([0.3, 0.05, 0.237, 0.04])
axSlider2 = fig.add_axes([0.3, 0.05, 0.237, 0.04])
axSlider2.set_xticks([])
axSlider2.set_yticks([])

slider1 = Slider(axSlider1, 'radial', 0.0, 50., valinit=25.)
slider2 = Slider(axSlider2, 'angular', 0.0, 20., valinit=10.)
freqRad, freqAng = slider1.val, slider2.val

# Filter angular sliders
axSlider3 = fig.add_axes([0.7, 0.125, 0.234, 0.04])
axSlider3.set_xticks([])
axSlider3.set_yticks([])

#axSlider4 = plt.axes([0.7, 0.05, 0.237, 0.04])
axSlider4 = fig.add_axes([0.7, 0.05, 0.237, 0.04])
axSlider4.set_xticks([])
axSlider4.set_yticks([])

slider3 = Slider(axSlider3, 'angle',  -np.pi, np.pi, valinit=0)
slider4 = Slider(axSlider4, 'thresh', -1., 1., valinit=0.)
angle, thresh = slider3.val, slider4.val

def update():
    radialImg = np.cos(distImg  * float(int(freqRad )))
    circumImg   = np.cos((angleImg + angle) * float(int(freqAng)))
    mergeImg  = (radialImg + circumImg)
    maskImg = (mergeImg > thresh)
    xmask = ma.make_mask(maskImg)
    filtImg = fourShft * xmask
    filtLog = np.log(np.maximum(np.abs(filtImg),1.))
    fourPlot.set_data(filtLog)
    plt.sca(axFourInv)    
    fourIshft = np.fft.ifftshift(filtImg)
    fourInv  = np.fft.ifft2(fourIshft)
    fourReal = np.real(fourInv)
#    invPlot = plt.imshow(fourReal, cmap='gray')   
    invPlot.set_data(fourReal)    
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
    global angle
    angle = slider3.val
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
 

