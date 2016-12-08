#!/Users/slehar/anaconda/bin/python
# TestMaskImageComplex.py
#

import numpy as np
import numpy.ma as ma
from pprint import pprint

print '\n\n\n==========\n==========\n==========\n\n'
print '===== In TestMaskImageComplex.py ====='
print '\n\n\n==========\n==========\n==========\n\n'

tdat = np.arange(-np.pi, np.pi, 2*np.pi/10)

print '\n===[ tdat ]==='
pprint(tdat)

sindat = np.sin(tdat)
print '\n===[ sindat ]==='
pprint(sindat)

cosdat = np.cos(tdat)
print '===[cosdat ]==='
pprint(cosdat)

complexdat = np.array(np.zeros(len(tdat), dtype=complex))
complexdat = sindat + 1j * cosdat 

print '/n===[ complexdat ]==='
pprint(complexdat)

l = complexdat
img=[l,l,l,l,l,l,l,l,l,l]

print '\n===[ img ]==='
pprint(img)

npImg = np.array(img)
print '\n===[ npImg ]==='
pprint(npImg)

l  = [False,False,False,False,False,False,False,False,False,False]
ll = [False,False,False,True, True, True,`True, False,False,False]
maskImg=[l,l,l,ll,ll,ll,ll,l,l,l]

print '\n===[ maskImg ]==='
pprint(maskImg)

npMask=np.array(maskImg, dtype=bool)

print '\n===[ npMask ]==='
pprint(npMask)

mask = ma.make_mask(npMask)

print '\n===[ mask ]==='
pprint(mask)

masked = npImg * mask

print '\n===[ masked ]==='
pprint(masked)





