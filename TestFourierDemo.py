# -*- coding: utf-8 -*-
"""
TestFourierDemo.py

Created on Thu Sep 29 09:57:55 2016

@author: slehar

From: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_transforms/py_fourier_transform/py_fourier_transform.html
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


img = mpimg.imread('Rover.png',0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magSpect = 20*np.log(np.abs(fshift))

plt.subplot(121)
plt.imshow(img, cmap = 'gray')
plt.title('Input Image')
plt.xticks([]), plt.yticks([])
plt.subplot(122)
plt.imshow(magSpect, cmap = 'gray', vmin=magSpect.min(),
                                                     vmax=magSpect.max())
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()

# Pop fig window to top
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 
