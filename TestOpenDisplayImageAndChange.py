# -*- coding: utf-8 -*-
"""
TestOpenDisplayImageAndChange.py

Created on Wed Sep 28 16:36:45 2016

@author: slehar
"""

import Tkinter, tkFileDialog
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# Get filename with Tkinter dialog
root = Tkinter.Tk()
root.withdraw()
imgFile = tkFileDialog.askopenfilename(
                    title='Select image',
                    initialfile = 'Rover.png')
# Read and display image
img = mpimg.imread(imgFile)
imgplot = plt.imshow(img)
plt.ion()
imgplot.axes.set_xticks([])
imgplot.axes.set_yticks([])
plt.show()

# Wait till keypress
raw_input('pause : press key to change ...')

# Paint a white square & update display
img[:100,:100] = 255.
imgplot.set_data(img)
plt.draw()
#plt.pause(.001)
#plt.show()

raw_input('pause : press key to quit ...')


figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
 

