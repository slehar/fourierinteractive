import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sys
import pdb

#### read an image and return its data with double precision
def readImage(filename):
    im = Image.open(filename)
#    data = np.zeros((width,height))
    data = np.array(im)
    return data.astype(float)  #float is double precision
    
#### generate sinusoidal image from scratch
def generateImage(freq):
    indexrow = np.linspace(0., 2.*np.pi*freq, num=128)
#    sinrow = (np.sin(indexrow) + 1.) * 128.
    sinrow = (np.sin(indexrow)) * 128.
    img = []
    for row in range(128):
        img.append(sinrow)
    return np.array(img)
    

#### swap first<-->third, second<-->fourth quadrant
def fftshift(data):
# assuming data is numpy 2d array
    nr = data.shape[0]
    nc = data.shape[1]
    assert (nr%2 == 0) & (nc%2 == 0)

    tmp = np.copy(data[0:nr/2,0:nc/2])
    data[0:nr/2,0:nc/2] = np.copy(data[nr/2:,nc/2:])
    data[nr/2:,nc/2:] = np.copy(tmp)

    tmp = np.copy(data[0:nr/2,nc/2:])
    data[0:nr/2,nc/2:] = np.copy(data[nr/2:,0:nc/2])
    data[nr/2:,0:nc/2] = np.copy(tmp)

#### normalize the FFT
def normalizefft(data):
    fftshift(data)
    #ndata = np.log(np.absolute(data)+1)
    ndata = np.absolute(data)
    ndata = ndata*255/ndata.max()

    return ndata

#### write image
def writeImage(data,filename):
    im = Image.fromarray(data)
    im.save(filename)


#### fft
def fft2d(data):
    
#    nr = data.shape[0]
#    nc = data.shape[1]
#    ndata = np.zeros((nr,nc),dtype=complex)
#
#    for i in range(nr):
#        ndata[i,:] = np.fft.fft(data[i,:])
#
#    for i in range(nc):
#        ndata[:,i] = np.fft.fft(ndata[:,i])


    ndata = np.fft.fft2(data)
    import code; code.interact(local=locals())

    return ndata

#### main
def main():


    ####### Open figure and set axes 1 ########
    plt.close('all')
    fig = plt.figure(figsize=(10,8))
    fig.canvas.set_window_title('fft1')
    
    #### Main axes ####
    ax = fig.add_axes([.1, .225, .7, .75])
#    ax.set_xticks([])
#    ax.set_yticks([])
    ax.set_xlim([0, 128])
    ax.set_ylim([0,255])


    outputname = "sin_fft.tif"
#    data = readImage(sys.argv[1])
    data = generateImage(4.0)
    ax.plot(data[64])
    print "type(data) = "+str(data.dtype)
    for j in range(63,66):
        for i in range(59,70):
            print '%05.2f '%data[j][i],
        print
    fftdata = np.fft.fft2(data)
   # fftdata1 = fft2d(data)
   # print np.allclose(fftdata,fftdata1)
    ndata = normalizefft(fftdata)
    ax.plot(ndata[64])
    for j in range(63,66):
        for i in range(59,70):
            print '%05.2f '%ndata[j][i],
        print
    ndata = ndata.astype('uint8')
#    pdb.set_trace()
    writeImage(ndata,outputname)

    # Show plot
    plt.show()

    # Gef fig manager to raise window in top left corner (10,10)
    figmgr=plt.get_current_fig_manager()
    figmgr.canvas.manager.window.raise_()
    geom=figmgr.window.geometry()
    (xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
    figmgr.window.setGeometry(10,10,dxWidth,dyHeight)




#### main call
if __name__ == "__main__":
    main()

