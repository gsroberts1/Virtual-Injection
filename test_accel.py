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


G1 = gradient(V[:,:,:,1])
G2 = gradient(V[:,:,:,2])

A1 = V[:,:,:,1]*G1[1] + V[:,:,:,2]*G1[2]
A2 = V[:,:,:,1]*G2[1] + V[:,:,:,2]*G2[2]

print(V.shape)

#figure()
#quiver(V[64,15:-15:4,15:-15:4,2], V[64,15:-15:4,15:-15:4,1],scale=50.0)
#
#figure()
#quiver(A1[2][64,:,:], A1[1][64,:,:])

figure()
imshow(A1[64,:,:])
colorbar()

figure()
imshow(A2[64,:,:])
colorbar()

#quiver(A2[2][64,:,:], A1[1][64,:,:])


show()