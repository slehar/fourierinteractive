# -*- coding: utf-8 -*-
"""
TestOpenDisplayAndFourierInverse.py

Created on Wed Sep 28 16:36:45 2016

@author: slehar
"""

import matplotlib.pyplot as plt
from PIL import Image
import Tkinter, tkFileDialog
import numpy as np
import sys

# Global Variables
rad1 = 0.125
rad2 = 0.6

# Get image using finder dialog
root = Tkinter.Tk()
root.withdraw() # Hide the root window
imgFile = tkFileDialog.askopenfilename(
    title = 'Select image',
    initialfile = 'Rover.png')

# Open figure window
winXSize = 16
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
imgNp = np.array(imgPil.convert('L'))
ySize, xSize = imgNp.shape
hafY, hafX = ySize//2, xSize//2
imgplot = plt.imshow(imgPil)

# Axes for Fourier Image
axFour = fig.add_axes([.3, .2, .7/winAspect, .7])
axFour.axes.set_xticks([])
axFour.axes.set_yticks([])
axFour.set_title('Fourier')

# Fourier Transform
fourImg  = np.fft.fft2(imgNp)
fourShft = np.fft.fftshift(fourImg)
fourLog  = np.log(np.abs(fourShft))

fourplot = plt.imshow(fourLog, cmap='gray',
                      vmin=fourLog.min(),
                      vmax=fourLog.max())

# Axes for Inverse Fourier Image
axFourInv = fig.add_axes([.56, .2, .7/winAspect, .7])
axFourInv.axes.set_xticks([])
axFourInv.axes.set_yticks([])
axFourInv.set_title('Inverse Fourier')

# Inverse Fourier Transform
fourIshft = np.fft.ifftshift(fourShft)
fourInv  = np.fft.ifft2(fourIshft)
fourReal = fourInv.astype(float)
plt.imshow(fourReal, cmap='gray',
                      vmin=fourReal.min(),
                      vmax=fourReal.max())
                      
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
 

