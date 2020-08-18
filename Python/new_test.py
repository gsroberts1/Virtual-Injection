from seed import *
from bPath import *
from toa import *
from PCVIPR import *
import numpy as np
import time

PLoader = PCVIPR('F:\\Virtual Injection\\140314_PATIENT_AVM\\PCVIPR')
CD = PLoader.getArray('CD.dat')
MAG = PLoader.getArray('MAG.dat')
VX = PLoader.getArray('comp_vd_1.dat')
VY = PLoader.getArray('comp_vd_2.dat')
VZ = PLoader.getArray('comp_vd_3.dat')

V = zeros((PLoader.resX, PLoader.resY, PLoader.resZ, 3))
V[:, :, :, 0] = VZ  # in mm/s
V[:, :, :, 1] = VY
V[:, :, :, 2] = VX

CD = CD.astype('double')  # change CD to double
CD = CD / CD.max()
thresh = 0.09
angio = CD > thresh

plt.figure()
plt.imshow(angio.max(0), cmap='gray')
plt.show()

CD[angio] = thresh  # anything above thresh=1, keep everything else same

conv = PLoader.resX / PLoader.fovX / 1000  # 320 pixels, 220 mm
V *= conv  # convert to pixels/ms


########### CALCULATE PATHLINES ##################

## Tracking/Sampling Flags
samplingType = 'spherical'  # define sampling type ('spherical' or 'plane')
reverseTrackingFlag = 0  # define direction of tracking

## Calculate pathlines
spread = 0.15
cutoff = 0.7
steps = 1200  # Iterations (steps*offset = time elapsed)
offset = 1  # Time increment (ms)
reducer = 2.0
max_paths = 10000
allpaths = []
start = time.clock()

## For reverse (venous) tracking
if reverseTrackingFlag == 1:
    V = -V
    offset = -offset

## Plane sampling
if samplingType == 'plane':
    zs = 205  # Select slice location
    width = 2  # Half width of slice
    plane = np.sum(CD[zs - width:zs + width, :, :], axis=0)  # get slice of width*2
    dplane = sign(np.sum(V[zs - width:zs + width, :, :, 0], axis=0))  # forward/reverse flow check
    plane[plane <= thresh] = 0  # Make plane binary based on threshold
    plane[plane > thresh] = 1

    plane[dplane < 0] = 0
    Xm, Ym = nonzero(plane)
    for i in range(max_paths):
        allpaths.append(bPath([sampleInPlane(Xm, Ym, zs)]))
elif samplingType == 'spherical':
    r0 = array([145, 160, 95])
    for i in range(int(max_paths)):
        allpaths.append(bPath([sampleInSphere(3.0, r0)]))
else:
    print('ERROR: Need to define a suitable sampling type ("spherical" or "plane").')


TOA = zeros(CD.shape)
stoppedpaths = []

for i in range(steps):
    print(('iteration: ' + str(i)))
    stepPathsDisplaceRand(allpaths, V, offset, CD, spread, cutoff, reducer, PLoader)

    print('Length: ' + str(len(allpaths)))

    TOA = TOA + TOAMap(allpaths, CD.shape, max_paths / len(allpaths))
    if (i + 1) % 25 == 0:
        savename = 'inject_data/TOAf1_t%04d.npy' % i
        print(savename)
        save(savename, TOA.astype('uint16'))

print(('Time: ' + str(time.process_time() - start)))

# figure()
# imshow(CD[:,60:200,:].max(1), origin='upper')
# set_cmap('gray')
# colorbar()
# for path in allpaths:
#    path.plot((2,0))
# for path in stoppedpaths:
#    path.plot((2,0))
# savefig('out2.png')
# show()
