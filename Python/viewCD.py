from pylab import *
from torusPhantom import torusPhantom
from sphericalSample import sampleInSphere
from bPath import *
import operator
from random import shuffle
from toa import *
from PCVIPR import PCVIPR
import time
import copy as cp
        
#PLoader = PCVIPR('/data/data_flow/HEAD_NECK/PATIENTS/ANEURYSM/130808_ANUR')
#PLoader = PCVIPR('/data/data_flow/HEAD_NECK/PATIENTS/AVM/130830_FISTULA')
#PLoader = PCVIPR('/data/data_flow/HEAD_NECK/PATIENTS/AVM/100913_PATIENT1/VIPR/ijt1/PCVIPR_RECON')
PLoader = PCVIPR('/data/data_flow/HEAD_NECK/ADRC_STUDY/100322_E486_S1000/PCVIPR_20111014')

CD = PLoader.getArray('CD.dat')

figure()
imshow(CD[:,:,:].max(2), origin='upper', vmax=1000)
set_cmap('gray')
colorbar()
savefig('/export/home/loecher/CD2.png')

figure()
imshow(CD[:,:,:].max(1), origin='upper',vmax=1000)
set_cmap('gray')
colorbar()
savefig('/export/home/loecher/CD1.png')

figure()
imshow(CD[:,:,:].max(0), origin='upper', vmax=1000)
set_cmap('gray')
colorbar()
savefig('/export/home/loecher/CD0.png')

#plane = sum(CD[256:258,:,:],axis=0)
#plane = CD[258:260,:,:].max(0)
#dplane = sign(sum(VZ[256:258,:,:],axis=0))
#
#thresh = 1500
#plane[plane<=thresh] = 0
#plane[plane>thresh] = 1
#
#plane[dplane<0] = 0
#
#print(flatnonzero(plane))
#
#imshow(plane, origin='upper', cmap='gray')
#colorbar()

#zs = 260
#width = 1
#thresh = 3000
#plane = sum(CD[zs-width:zs+width,:,:],axis=0)
#dplane = sign(sum(VZ[zs-width:zs+width,:,:],axis=0))
#
#plane[plane<=thresh] = 0
#plane[plane>thresh] = 1
#
#plane[dplane<0] = 0
#figure()
#imshow(plane, origin='upper', cmap='gray')
show()