# TestMaskImage.py
#

import numpy as np
import numpy.ma as ma
from pprint import pprint

l = range(10)
img=[l,l,l,l,l,l,l,l,l,l]

print '\n===[ img ]==='
pprint(img)

print '\n===[ npImg ]==='
npImg = np.array(img)

l  = [False,False,False,False,False,False,False,False,False,False]
ll = [False,False,False,True,True,True,True,False,False,False]
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





