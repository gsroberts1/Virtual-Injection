from pylab import *
from torusPhantom import torusPhantom
from seed import *
from bPath import *
import operator
from random import shuffle
from toa import *
from PCVIPR import PCVIPR
import time
import copy as cp
    
PLoader = PCVIPR('D:\\Patients\\FILLTHISIN\\FILLTHISIN\\dat\\CORRECTED')
CD = PLoader.getArray('CD.dat')
VX = PLoader.getArray('comp_vd_1.dat')
VY = PLoader.getArray('comp_vd_2.dat')
VZ = PLoader.getArray('comp_vd_3.dat')

V = zeros((VX.shape[0],VX.shape[1],VX.shape[2],3))
V[:,:,:,0] = -VZ
V[:,:,:,1] = -VY
V[:,:,:,2] = -VX

P = copy(CD).astype('double')
thresh1 = 2000 ### Adjust this

plt.figure()
plt.imshow((P>thresh1).max(0)) 
plt.show()

Phigh = thresh1
P[P > Phigh] = Phigh

#Plow = 500
#P[P < Plow] = 0

Pmax = P.max()
P *= 1/Pmax

# V is in mm/s
conv = 320/220/1000  # 320 pixels, 220 mm
V *= conv  # convert to pixels/ms

zs = 42
width = 1
thresh = 100
plane = sum(CD[:,:,zs-width:zs+width],axis=2) # Start plane (near base of skull)
dplane = sign(sum(VZ[:,:,zs-width:zs+width],axis=2))

plane[plane<=thresh] = 0
plane[plane>thresh] = 1

plane[dplane<0] = 0
Xm, Ym = nonzero(plane)

# Bolus creation
allpaths = []
max_paths = 10000
#r0 = array([260,139.5,119]) #carotid1
#r0 = array([300,197,158.5]) #carotid2
#r0 = array([229,163,161]) #basilar
#r0 = array([134,82,132]) #AVM
#r0 = array([226,147.5,186]) #carotid1 hgih
#for i in range(int(max_paths/2)):
#    allpaths.append(bPath( [sampleInSphere(1.0,r0)] ))
#r0 = array([260,139.5,198]) #carotid2
#for i in range(int(max_paths/2)):
#    allpaths.append(bPath( [sampleInSphere(1.0,r0)] ))
    
for i in range(max_paths):
    allpaths.append(bPath( [sampleInPlane(Xm, Ym, zs)] ))

# Calculate pathlines
spread = 0.15
cutoff = 0.7    #0.9
steps = 1200
offset = 2.5
reducer = 2.0
start = time.clock()

#V = -V
#offset = -offset

TOA = zeros(P.shape)

stoppedpaths = []

for i in range(steps):
    print(('iteration: ' + str(i)))
    stepPathsDisplaceRand(allpaths, V, offset, P, spread, cutoff, reducer)
    
    print('Length: ' + str(len(allpaths)))
    
    TOA = TOA + TOAMap(allpaths, P.shape, max_paths/len(allpaths))
    if (i+1)%30 == 0:
        savename = 'inject_data/TOAf1_t%04d.npy' % i
        print(savename)
        save(savename, TOA.astype('uint16'))
    
print(('Time: ' + str(time.clock()-start)))

#figure()
#imshow(CD.max(2), origin='upper', interpolation='none')
#set_cmap('gray')
#colorbar()
#for path in allpaths:
#    path.plot((1,0))
##savefig('out12.eps')
#    
#figure()
#imshow(CD[:,60:200,:].max(1), origin='upper')
#set_cmap('gray')
#colorbar()
#for path in allpaths:
#    path.plot((2,0))
#for path in stoppedpaths:
#    path.plot((2,0))
##savefig('out2.png')
#show()
