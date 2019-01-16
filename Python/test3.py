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

from multiprocessing import Process, Queue

def mpPathSteps(allpaths, V, P, splits, spread, ncpu):
    def worker(paths, V, P, splits, spread, out_q):
        for i in range(len(paths)):
            paths.extend(paths[i].stepAlong(V,P,splits,spread))
        out_q.put(paths)
        
    out_q = Queue()
    chunksize = int(math.ceil(len(allpaths) / float(ncpu)))
    procs = []
    
    for i in range(ncpu):
        p = Process(target=worker,
                    args=(allpaths[chunksize * i:chunksize * (i+1)],
                          V, P, splits, spread, out_q))
        procs.append(p)
        p.start()
    
    outpaths = []
    for i in range(ncpu):
        outpaths.extend(out_q.get())
        
    for p in procs:
        p.join()
        
    return outpaths
        
    
PLoader = PCVIPR('/data/data_flow/HEAD_NECK/PATIENTS/AVM/100913_PATIENT1/VIPR/ijt1/PCVIPR_RECON')
CD = PLoader.getArray('CD.dat')
VX = PLoader.getArray('comp_vd_1.dat')
VY = PLoader.getArray('comp_vd_2.dat')
VZ = PLoader.getArray('comp_vd_3.dat')

V = zeros((VX.shape[0],VX.shape[1],VX.shape[2],3))
V[:,:,:,0] = -VZ
V[:,:,:,1] = -VY
V[:,:,:,2] = -VX

P = copy(CD)

Phigh = 2500
P[P > Phigh] = Phigh
P = P / P.max()


V = V*320/220/1000 #convert to pixels/ms

#CD[287:289, 196:198, 161:163] = 2

# Bolus creation
allpaths = []
max_paths = 500
r0 = array([300,133,162])
#r0 = array([226,147.5,186])
for i in range(max_paths):
    allpaths.append(bPath( [sampleInSphere(1.5,r0)] ))
    
    
# Calculate pathlines
splits = 5
spread = 0.1
cutoff = 0.8
steps = 800
offset = 2.7
start = time.clock()

TOA = zeros(P.shape)

stoppedpaths = []

for i in range(steps):
    print(('iteration: ' + str(i)))
    #allpaths = mpPathSteps(allpaths, V, P, splits, spread, 8)
    #for j in range(len(allpaths)):
    #    allpaths.extend(allpaths[j].stepAlong(V,P,splits,spread))
    stoppedpaths.extend(stepPathsDisplaceRand(allpaths, V, offset, P, spread, cutoff))
    
    #allpaths = randomizeSplit(allpaths, P, splits, spread)
    print((len(allpaths)))
    print((len(stoppedpaths)))
    
    TOA = TOA + TOAMap(allpaths, P.shape)
    #if (i+1)%20 == 0:
    #    save('/data/loecher/INJECT/TOAb1_t%03d.npy' % i, TOA.astype('uint16'))
    #if (len(allpaths)>max_paths):
    #    allpaths.sort(key=operator.attrgetter('prob'), reverse=True)
    #    j = 0
    #    while (j<len(allpaths)) and (allpaths[j].prob>cutoff):
    #        j = j+1
    #    print(j)
    #    allpaths = allpaths[:j]
    #    shuffle(allpaths)
    #    allpaths = allpaths[:max_paths]
    ##if ((i%5)==0):
    ##    TOASmear(allpaths, P.shape)
    
print(('Time: ' + str(time.clock()-start)))

#figure()
#imshow(CD.max(2), origin='upper', interpolation='none')
##pcolormesh(CD.max(2))
#set_cmap('gray')
#colorbar()
#t = 79
#for path in allpaths:
#    path.plot((1,0))
#for path in stoppedpaths:
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