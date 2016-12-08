# TestMin.py
#

import numpy as np

ramp = np.array(np.arange(-1,1,.05))

print '\n===[ ramp ]==='
for num in ramp:
    print '%5.2f '%num
print

print '\n===[ rampmin ]=='
rampmin = np.maximum(ramp, 0.25)
for num in rampmin:
    print '%5.2f '%num
print
