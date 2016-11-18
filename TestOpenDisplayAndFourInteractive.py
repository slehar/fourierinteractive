# -*- coding: utf-8 -*-
"""
TestOpenDisplayAndFourInteractive.py

Created on Wed Sep 28 16:36:45 2016

@author: slehar
"""

import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider
from   PIL import Image
import Tkinter, tkFileDialog
import numpy as np
import numpy.ma as ma
import sys


def maxmin(img):
    print '(max, min) = (%5.2f, %5.2f)'%(img.max(),img.min())

# Global Variables
rad1 = .15
rad2 = 0.

# Get image using finder dialog
root = Tkinter.Tk()
root.withdraw() # Hide the root window
imgFile = tkFileDialog.askopenfilename(
    title = 'Select image',
    initialfile = 'Rover.png')

# Open figure window
winXSize = 18
winYSize = 6
winAspect = winXSize/winYSize
plt.close('all')
fig = plt.figure(figsize=(winXSize, winYSize))

# Keypress 'q' to quit callback function
def press(event):
    global ptList, data
    sys.stdout.flush()
    if event.key == 'q':
        plt.close()

# Connect keypress event to callback function
fig.canvas.mpl_connect('key_press_event', press)

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

plt.pause(3.)

# Fourier Filtering
yy, xx = np.mgrid[-hafY:hafY, -hafX:hafX]
distImg = np.sqrt(xx**2 + yy**2)
maskImg = (distImg < (rad1 * xSize))
xmask = ma.make_mask(maskImg)

#maskImg[hafY, hafX] = True
filtImg = np.real(fourShft) * xmask

filtImg[filtImg < 0.] = 0.
fourLog1 = np.log(np.abs(filtImg))

#fourPlot = plt.imshow(magSpect, cmap='gray',
#                      vmin=magSpect.min(),
#                      vmax=magSpect.max())
fourPlot = plt.imshow(fourLog1, cmap='gray',
                      vmin=fourLog1.min(),
                      vmax=fourLog1.max())
plt.pause(.001)

# Axes for Inverse Fourier Image
axFourInv = fig.add_axes([.56, .2, .7/winAspect, .7])
axFourInv.axes.set_xticks([])
axFourInv.axes.set_yticks([])
axFourInv.set_title('Inverse Fourier')

# Inverse Fourier Transform
fourIshft = np.fft.ifftshift(fourShft)
fourInv  = np.fft.ifft2(fourIshft)
fourReal = np.real(fourInv)
invPlot = plt.imshow(fourReal, cmap='gray')

# Filter radius sliders
#axSlider1 = plt.axes([0.3, 0.125, 0.234, 0.04])
axSlider1 = fig.add_axes([0.3, 0.125, 0.234, 0.04])
axSlider1.set_xticks([])
axSlider1.set_yticks([])

axSlider2 = plt.axes([0.3, 0.05, 0.237, 0.04])
axSlider2 = fig.add_axes([0.3, 0.05, 0.237, 0.04])
axSlider2.set_xticks([])
axSlider2.set_yticks([])

slider1 = Slider(axSlider1, 'r1', 0.0, xSize, valinit=xSize*rad1)
slider2 = Slider(axSlider2, 'r2', 0.0, xSize, valinit=xSize*rad2)

def update(val):
    global rad1, filtImg
#    plt.sca(axFour)
    rad1 = slider1.val
    print 'rad1 = %5.2f'%rad1
    rad2 = slider2.val
    maskImg = (distImg < (rad1 * xSize))
    print maskImg[180,150:170]
    xmask = ma.make_mask(maskImg)
#    maskImg[hafY,hafX] = False
    filtImg[filtImg < 0.] = 0.
    filtImg = fourShft * xmask
    fourLog2 = np.log(np.abs(filtImg))
    fourLog2[hafY:hafY+20,hafX:hafX+20] = val
#    print newSpect[hafY-4:hafY+5, hafX-4:hafX+5]
#    fourPlot.set_data(filtImg)
    fourPlot.set_data(fourLog2)
    fourPlot.set_clim(fourLog2.min(), fourLog2.max())
    plt.draw()
#    plt.show(block=False)
#    plt.show()
    plt.pause(.001)

#    fig.canvas.draw()
slider1.on_changed(update)
slider2.on_changed(update)

# Show image
plt.ion()
plt.sca(axFour)
#plt.pause(.001)
plt.show()

#for ii in range(5):
#    print 'Calling update(%1d)'%ii
#    update(ii)


# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 

