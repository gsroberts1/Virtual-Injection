from pylab import *
from torusPhantom import torusPhantom
from sphericalSample import sampleInSphere
from bPath import *
import operator
from random import shuffle
from toa import *

IM0 = torusPhantom(offset=-0.1)[0]

noise_scale = 0.3
noiser = randn(IM0.shape[0], IM0.shape[1], IM0.shape[2], IM0.shape[3])
noisei = randn(IM0.shape[0], IM0.shape[1], IM0.shape[2], IM0.shape[3])

IM = IM0 + noise_scale*(noiser + 1j*noisei)

P = abs(IM[:,:,:,0])/2.0

V = angle(IM)

# Bolus creation
allpaths = []
max_paths = 20
r0 = array([64,64,102])
for i in range(max_paths):
    allpaths.append(bPath( [sampleInSphere(3,r0)] ))    

# Calculate pathlines
for i in range(80):
    print(i)
    stepPathsDisplace(allpaths, V, 2.2)


imshow(P[64,:,:], origin='lower')
set_cmap('gray')
#imshow(abs(IM0[:,:,64,0]))
colorbar()
for path in allpaths:
    path.plot((1,2))

show()