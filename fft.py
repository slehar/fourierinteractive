import numpy as np
from PIL import Image
import sys
import pdb

#### read an image and return its data with double precision
def readImage(filename):
    im = Image.open(filename)
    width = im.width
    height = im.height
#    data = np.zeros((width,height))
    data = np.array(im)
    return data.astype(float)  #float is double precision

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
    ndata = np.log(np.absolute(data)+1)
    #ndata = np.absolute(data)
    ndata = ndata*255/ndata.max()

    return ndata

#### write image
def writeImage(data,filename):
    im = Image.fromarray(data)
    im.save(filename)


#### fft
def fft2d(data):
    nr = data.shape[0]
    nc = data.shape[1]
    ndata = np.zeros((nr,nc),dtype=complex)

    for i in range(nr):
        ndata[i,:] = np.fft.fft(data[i,:])

    for i in range(nc):
        ndata[:,i] = np.fft.fft(ndata[:,i])

    return ndata

#### main
def main():

    outputname = sys.argv[1] + "_fft.tif"
    data = readImage(sys.argv[1])
    fftdata = np.fft.fft2(data)
   # fftdata1 = fft2d(data)
   # print np.allclose(fftdata,fftdata1)
    ndata = normalizefft(fftdata)
    ndata = ndata.astype('uint8')
    writeImage(ndata,outputname)

#### main call
if __name__ == "__main__":
    main()

