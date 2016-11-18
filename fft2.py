import numpy as np
from PIL import Image
import sys
import pdb



#read an image and return its data with double precision
def readImage(filename):
    im = Image.open(filename)
#    data = np.zeros((width,height))
    data = np.array(im)
    return data.astype(float)  #float is double precision

# swap first<-->third, second<-->fourth quadrant
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

def normalizefft(data):
    fftshift(data)
    #ndata = np.log(np.absolute(data)+1)
    ndata = np.absolute(data)
    ndata = ndata*255/ndata.max()

    return ndata


def writeImage(data,filename):
    im = Image.fromarray(data)
    im.save(filename)


def generateImage(freq,filename):
    indexrow = np.linspace(0., 2.*np.pi*freq, num=128)
    sinrow = (np.sin(indexrow) + 1.) * 128.
    img = []
    for row in range(128):
        img.append(sinrow)
#    return np.array(img)
    img = np.array(img,dtype='uint8')
    fimg  = Image.fromarray(img)
    fimg.save(filename)



def fft2d(data):
    nr = data.shape[0]
    nc = data.shape[1]
    ndata = np.zeros((nr,nc),dtype=complex)

    for i in range(nr):
        ndata[i,:] = np.fft.fft(data[i,:])

    for i in range(nc):
        ndata[:,i] = np.fft.fft(ndata[:,i])

    return ndata


def main():

#    generateImage(float(sys.argv[1]),sys.argv[2])
    generateImage(3, 'sin3.gif')
    outputname = "sin3_fft.tif"
    data = readImage('sin3.gif')
    fftdata = np.fft.fft2(data)
    ndata = normalizefft(fftdata)
    ndata = ndata.astype('uint8')
    writeImage(ndata,outputname)

if __name__ == "__main__":
    main()

