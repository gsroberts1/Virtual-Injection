from pylab import *
from torusPhantom import torusPhantom
from sphericalSample import sampleInSphere
from bPath import *
import operator
from random import shuffle
from toa import *

IM0 = torusPhantom(offset=-0.00)[0]

noise_scale = 0.0
noiser = randn(IM0.shape[0], IM0.shape[1], IM0.shape[2], IM0.shape[3])
noisei = randn(IM0.shape[0], IM0.shape[1], IM0.shape[2], IM0.shape[3])

IM = IM0 + noise_scale*(noiser + 1j*noisei)

P = abs(IM[:,:,:,0])/2.0

V = angle(IM)

print(V.shape)

# Bolus creation
allpaths = []
max_paths = 10
r0 = array([64,102,64])
for i in range(max_paths):
    allpaths.append(bPath( [sampleInSphere(3,r0)] ))    

# Calculate pathlines
for i in range(20):
    stepPathsDisplace(allpaths, V, 0.0)


imshow(P[64,15:-15,15:-15], extent=[0, 98, 0, 98])
set_cmap('gray')
colorbar()
for path in allpaths:
    path.plot((2,1),15)

#quiver(V[64,15:-15:4,15:-15:4,2], V[64,15:-15:4,15:-15:4,1],scale=50.0)

show()