# -*- coding: utf-8 -*-
"""
TestOpenDisplayImage.py

Created on Wed Sep 28 16:36:45 2016

@author: slehar
"""

import Tkinter, tkFileDialog
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
#import pylab

root = Tkinter.Tk()
#root.Font(family="Times", size=10, weight=tkFont.BOLD)
root.withdraw()

imgFile = tkFileDialog.askopenfilename(title='Select image')

img = mpimg.imread(imgFile)
imgplot = plt.imshow(img)
imgplot.axes.set_xticks([])
imgplot.axes.set_yticks([])

figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 

