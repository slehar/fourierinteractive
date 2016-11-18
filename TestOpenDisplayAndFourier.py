# -*- coding: utf-8 -*-
"""
TestOpenDisplayAndFourier.py

Created on Wed Sep 28 16:36:45 2016

@author: slehar
"""

import matplotlib.pyplot as plt
from PIL import Image
import Tkinter, tkFileDialog
import numpy as np

# Get image using finder dialog
root = Tkinter.Tk()
root.withdraw() # Hide the root window
imgFile = tkFileDialog.askopenfilename(
    title='Select image',
    initialfile='Rover.png')

# Open figure window
winXSize = 12
winYSize = 6
winAspect = winXSize/winYSize
fig = plt.figure(figsize=(winXSize, winYSize))

# Axes for Original Image
axOrig = fig.add_axes([.1, .2, .7/winAspect, .7])
axOrig.axes.set_xticks([])
axOrig.axes.set_yticks([])

# Read image and display
imgPil = Image.open(imgFile).convert('LA')
imgNp = np.array(imgPil.convert('L'))
imgplot = plt.imshow(imgPil)

# Axes for Fourier Image
axFour = fig.add_axes([.5, .2, .7/winAspect, .7])
axFour.axes.set_xticks([])
axFour.axes.set_yticks([])

# Fourier Transform
fourImg  = np.fft.fft2(imgNp)
fourShft = np.fft.fftshift(fourImg)

magSpect = 20*np.log(np.abs(fourShft))

absShft  = np.absolute(magSpect)
realShft = np.real(absShft)
normShft = realShft*255/realShft.max()
fourplot = plt.imshow(realShft, cmap = 'gray')

# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 

