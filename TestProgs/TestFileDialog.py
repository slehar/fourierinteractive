# -*- coding: utf-8 -*-
"""
TestFileDialog.py

From http://stackoverflow.com/questions/17435360/matplotlib-figures-not-working-after-tkinter-file-dialog
Created on Wed Sep 28 08:20:23 2016

@author: slehar
"""

import Tkinter, tkFileDialog
import pylab

root = Tkinter.Tk()
print 'root = %r'%root
root.withdraw()

file_path = tkFileDialog.askopenfilename()

#file_path = tkFileDialog.askopenfilename(
#    parent=root,
#    mode='rb',
#    title='Choose a file')
    
print 'File path = %s'%file_path
 
pylab.figure()
pylab.show()
 
print "Made it."
 

