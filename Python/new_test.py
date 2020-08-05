from seed import *
from bPath import *
from toa import *
from PCVIPR import *
import time

PLoader = PCVIPR('F:\\Virtual Injection\\140314_PATIENT_AVM\\PCVIPR')
sizex = PLoader.resX
fovx = PLoader.fovX
CD = PLoader.getArray('CD.dat')
MAG = PLoader.getArray('MAG.dat')
VX = PLoader.getArray('comp_vd_1.dat')
VY = PLoader.getArray('comp_vd_2.dat')
VZ = PLoader.getArray('comp_vd_3.dat')

V = zeros((VX.shape[0], VX.shape[1], VX.shape[2], 3))
V[:, :, :, 0] = -VZ  # in mm/s
V[:, :, :, 1] = -VY
V[:, :, :, 2] = -VX

P = copy(CD).astype('double')
thresh1 = 3000

plt.figure()
plt.imshow((P > thresh1).max(0))
plt.show()

Phigh = thresh1
P[P > Phigh] = Phigh

Pmax = P.max()
P *= 1 / Pmax

conv = sizex / fovx / 1000  # 320 pixels, 220 mm
V *= conv  # convert to pixels/ms

###### PLANE SELECTION ######
# zs = 205 # Select slice location
# width = 2 # Width of slice
# thresh = 4000
# plane = sum(CD[zs-width:zs+width,:,:],axis=0) # Start plane (near base of skull)
# dplane = sign(sum(VZ[zs-width:zs+width,:,:],axis=0))

# plane[plane<=thresh] = 0
# plane[plane>thresh] = 1

# plane[dplane<0] = 0
# plane[dplane>0] = 0
# Xm, Ym = nonzero(plane)
###########################

# Bolus creation
allpaths = []
max_paths = 10000

r0 = array([145, 160, 95])  # AVM2
for i in range(int(max_paths / 2)):
    allpaths.append(bPath([sampleInSphere(3.0, r0)]))

# Calculate pathlines
spread = 0.15
cutoff = 0.7  # 0.9
steps = 1200  # Iterations (steps*offset = time elapsed)
offset = 1  # Time increment (ms)
reducer = 2.0
start = time.clock()

##### REVERSE TRACKING ######
# V = -V
# offset = -offset
#############################

TOA = zeros(P.shape)

stoppedpaths = []

for i in range(steps):
    print(('iteration: ' + str(i)))
    stepPathsDisplaceRand(allpaths, V, offset, P, spread, cutoff, reducer)

    print('Length: ' + str(len(allpaths)))

    TOA = TOA + TOAMap(allpaths, P.shape, max_paths / len(allpaths))
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
