from pylab import *
from torusPhantom import torusPhantom
from interpolate import interpolate3D3Dpoint
from bPath import bPath

IM0 = torusPhantom()[0]

noise_scale = 1.0
noiser = randn(IM0.shape[0], IM0.shape[1], IM0.shape[2], IM0.shape[3])
noisei = randn(IM0.shape[0], IM0.shape[1], IM0.shape[2], IM0.shape[3])

IM = IM0 + noise_scale*(noiser + 1j*noisei)

VX = angle(IM[:,:,:,0])
VY = angle(IM[:,:,:,1])
VZ = angle(IM[:,:,:,2])

tp = 5000;
h = .1

pos = empty([3,tp])
pos[0,0] = 102
pos[1,0] = 64
pos[2,0] = 64
for i in range(tp-1):
    pos[:,i+1] = pos[:,i]+interpolate3D3Dpoint(VX,VY,VZ,pos[:,i])*h

posrk = empty([3,tp])
posrk[0,0] = 102
posrk[1,0] = 64
posrk[2,0] = 64
for i in range(tp-1):
    k1 = interpolate3D3Dpoint(VX,VY,VZ,posrk[:,i])
    k2 = interpolate3D3Dpoint(VX,VY,VZ,posrk[:,i]+h/2*k1)
    k3 = interpolate3D3Dpoint(VX,VY,VZ,posrk[:,i]+h/2*k2)
    k4 = interpolate3D3Dpoint(VX,VY,VZ,posrk[:,i]+h*k3)
    posrk[:,i+1] = posrk[:,i] + h/6*(k1 + 2*k2 + 2*k3 + k4)

imshow(abs(IM0[:,:,64,1]))
colorbar()
plot(pos[0,:],pos[1,:])
plot(posrk[0,:],posrk[1,:],'g')
show()