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
PLoader = PCVIPR('D:\\Virtual_Injection_Data\\AVM\\130830_FISTULA\\PCVIPR')
sizex = PLoader.resX
fovx = PLoader.fovX
CD = PLoader.getArray('CD.dat')
MAG = PLoader.getArray('MAG.dat')
VX = PLoader.getArray('comp_vd_1.dat')
VY = PLoader.getArray('comp_vd_2.dat')
VZ = PLoader.getArray('comp_vd_3.dat')

f, axarr = plt.subplots(3,3)
axarr[0,0].imshow(CD[235,:,:])
axarr[0,1].imshow(CD[236,:,:])
axarr[0,2].imshow(CD[237,:,:])
axarr[1,0].imshow(CD[238,:,:])
axarr[1,1].imshow(CD[239,:,:])
axarr[1,2].imshow(CD[240,:,:])
axarr[2,0].imshow(CD[241,:,:])
axarr[2,1].imshow(CD[242,:,:])
axarr[2,2].imshow(CD[243,:,:])
plt.show()
