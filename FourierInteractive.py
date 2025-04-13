"""
FourInteractive.py

Created on Wed Sep 28 16:36:45 2016

Available on my GitHub site 

@author: slehar
"""

#%% Imports
import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider
from   matplotlib.widgets import CheckButtons
from   matplotlib.widgets import Button
import numpy as np
import numpy.ma as ma
from   PIL import Image
import tkinter as tk
import tkinter.filedialog
import sys

#%%  Global Variables
rad1 = 0.01
rad2 = 125.
slidersLocked = False
angle = 0.
angleThresh =  -1.
    
#%% Get image filename using finder dialog
root = tk.Tk()
# root.withdraw() # Hide the root window
imgFile = tk.filedialog.askopenfilename(initialfile = 'Rover.png',
                                        initialdir='.')
root.update()
root.quit()

# imgFile = 'Rover.png'

#%% Open figure window
winXSize = 16
winYSize = 6
winAspect = winXSize/winYSize
plt.close('all')
fig = plt.figure(figsize=(winXSize, winYSize))
fig.suptitle("Fourier Interactive", fontsize=18)

#%% Keypress 'q' to quit callback function
def press(event):
    global ptList, data
    sys.stdout.flush()
    if event.key == 'q':
        plt.close()
# Connect keypress event to callback function
fig.canvas.mpl_connect('key_press_event', press)

#%% Lock Sliders Checkbox
rax = plt.axes([0.2, 0.05, 0.1/winAspect, 0.1])
check = CheckButtons(rax, [' Lock'], [False])
def func(label):
    global slidersLocked
    
    if   label == ' Lock':
        slidersLocked = check.lines[0][0].get_visible()
    plt.draw()
check.on_clicked(func)


#%% Load Image Button

# axButt = fig.add.axes([0.1, 0.05, 0.1/winAspect, 0.2])
axButt = plt.axes([0.1, 0.05, 0.2/winAspect, 0.1])

Butt = Button(axButt, 'Load Image')
def buttFunc(self):
    print('Button Pressed')
Butt.on_clicked(buttFunc)
    
#%% Filter slider Axes

# slider1 Radius1 slider
axSlider1 = fig.add_axes([0.3, 0.125, 0.234, 0.04])
axSlider1.set_xticks([])
axSlider1.set_yticks([])

# axSlider2 = plt.axes([0.3, 0.05, 0.237, 0.04])
# slider 2 Radius2 slider
axSlider2 = fig.add_axes([0.3, 0.05, 0.237, 0.04])
axSlider2.set_xticks([])
axSlider2.set_yticks([])

# slider3 Angular slider
axSlider3 = fig.add_axes([0.7, 0.125, 0.234, 0.04])
axSlider3.set_xticks([])
axSlider3.set_yticks([])

#axSlider4 = plt.axes([0.7, 0.05, 0.237, 0.04])
# slider4 Angular Threshold slider
axSlider4 = fig.add_axes([0.7, 0.05, 0.237, 0.04])
axSlider4.set_xticks([])
axSlider4.set_yticks([])

#%% Axes for Original Image
axOrig = fig.add_axes([.05, .2, .7/winAspect, .7])
axOrig.axes.set_xticks([])
axOrig.axes.set_yticks([])
axOrig.set_title('Original')

#%% Read image into numpy array
imgPil = Image.open(imgFile).convert("LA")
imgNp = np.array(imgPil.convert('L'))/255.
npYSize, npXSize = imgNp.shape
hafY, hafX = int(npYSize/2), int(npXSize/2)
imgPlot = plt.imshow(imgPil, cmap='gray')

# axOrig.set_data(imgPil)


#%% Define Filter Sliders
# Filter Sliders
slider1 = Slider(axSlider1, 'r1', 0.0, npXSize, valinit=92)
slider2 = Slider(axSlider2, 'r2', 0.0, npXSize, valinit=142)
# freqRad, freqAng = slider1.val, slider2.val
rad1, rad2 = slider1.val, slider2.val


slider3 = Slider(axSlider3, 'angle',  -np.pi, np.pi, valinit=-1.5)
slider4 = Slider(axSlider4, 'thresh', -1., 1., valinit=-.3)
angle, angleThresh = slider3.val, slider4.val


#%% Axes for Fourier Image
axFour = fig.add_axes([.3, .2, .7/winAspect, .7])
axFour.axes.set_xticks([])
axFour.axes.set_yticks([])
axFour.set_title('Fourier')

#%% Fourier Transform
fourImg  = np.fft.fft2(imgNp)
fourShft = np.fft.fftshift(fourImg)
fourLog  = np.log(np.abs(fourShft))
plt.pause(.001)
plt.sca(axFour)
fourPlot = plt.imshow(fourLog, cmap='gray')
# fourPlot = plt.imshow(imgPil, cmap='gray')
# fourPlot.set_data(fourLog)
plt.show()


#%% Fourier Filtering
yy, xx = np.mgrid[-hafY:hafY, -hafX:hafX]
distImg = np.sqrt(xx**2 + yy**2)

angleImg = np.arctan2(yy,xx)
angleImgFlip = np.fliplr(np.flipud(angleImg))

maskR1 = (distImg > rad1)
maskR2 = (distImg < rad2)
maskRadial = np.logical_and(maskR1, maskR2)

maskAngle = (np.sin(angleImg*2. + angle) >= angleThresh)          
maskImg = np.logical_and(maskAngle, maskRadial)  
maskImg[hafY,hafX] = True

maskRadAng = ma.make_mask(maskImg)
filtImg = fourShft * maskRadAng
filtLog = np.log(np.maximum(np.abs(filtImg),1.))
FourPlot = plt.imshow(filtLog, cmap='gray')
# ??? FourPlot.set_data(filtLog)

plt.pause(.001)


#%% Axes for Inverse Fourier Image
axFourInv = fig.add_axes([.56, .2, .7/winAspect, .7])
axFourInv.axes.set_xticks([])
axFourInv.axes.set_yticks([])
axFourInv.set_title('Inverse Fourier')

#%% Inverse Fourier Transform
fourIshft = np.fft.ifftshift(filtImg)
fourInv   = np.fft.ifft2(fourIshft)
fourInvReal  = np.real(fourInv)
fourInvPlot = plt.imshow(fourInvReal, cmap='gray')
plt.sca(axFourInv)
invPlot = plt.imshow(fourInvReal, cmap='gray')
# invPlot.set_data(fourInvReal)




#%% update
def update():
    global rad1, rad2
    
    # plt.sca(axFour)
    maskR1 = (distImg > rad1)
    maskR2 = (distImg < rad2)
    maskRadial = np.logical_and(maskR1, maskR2)
    maskAngle = (np.sin(angleImg*2. + angle) >= angleThresh)          
    maskRadAngle = np.logical_and(maskAngle, maskRadial)  
    maskRadAngle[hafY,hafX] = True
    maMask = ma.make_mask(maskRadAngle)
    
    plt.sca(axFour)    
    filtImg = fourShft * maMask
    filtLog = np.log(np.maximum(np.abs(filtImg),1.))
    
    filtPlot = plt.imshow(filtLog, cmap='gray')   
    # filtPlot.set_data(filtLog)
    
    plt.sca(axFourInv)    
    fourIshft = np.fft.ifftshift(filtImg)
    fourInv  = np.fft.ifft2(fourIshft)
    fourInvReal = np.real(fourInv)
    
    fourInvPlot = plt.imshow(fourInvReal, cmap='gray')
    # fourInvPlot.set_data(fourInvReal)
    
    plt.pause(.001)
    plt.show()

#%% Update sliders
def update1(val):
    global rad1, rad2
    oldRad1 = rad1
    rad1 = slider1.val
    radRatio = rad1 / oldRad1
    if slidersLocked:
        rad2 = min((slider2.val * radRatio), npXSize)
        slider2.val = rad2
    update()

def update2(val):
    global rad1, rad2
    oldRad2 = rad2
    rad2 = slider2.val  
    radRatio = rad2 / oldRad2
    if slidersLocked:       
        rad1 = rad1 * radRatio
        if rad1 < 0:
            rad1 = 0
        slider1.set_val(rad1)
        plt.show()
    update()

def update3(val):
    global angle
    angle = slider3.val
    update()

def update4(val):
    global angleThresh
    angleThresh = slider4.val
    update()

#%% Attach sliders to their callback functions
slider1.on_changed(update1)
slider2.on_changed(update2)
slider3.on_changed(update3)
slider4.on_changed(update4)

#%% Show Image

# Show image
plt.sca(axFour)
plt.show()


