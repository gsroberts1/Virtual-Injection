from pylab import *
from interpolate_testcy import *
import operator
from collections import deque
import copy as cp

class bPath:
    
    def __init__(self, initPath):
        self.pos = list(initPath)
        self.prob = 1.0
        self.h = 3.0
        self.KE = 1.0
        self.plength = 4
        self.plist = deque([1.0,]*self.plength)
        
    def stepAlong(self, V, P, split=0, spread = 0.1):
        
        # Copy extra probabalistic paths
        out = []
        for i in range(split):
            out.append(bPath(self.pos))
            out[i].prob = self.prob
            out[i].plist = deque(self.plist)
        
        # Calculate deterministic step 
        k1 = interpolate3D3Dpoint(V,self.pos[-1])
        k2 = interpolate3D3Dpoint(V,self.pos[-1]+self.h/2*k1)
        k3 = interpolate3D3Dpoint(V,self.pos[-1]+self.h/2*k2)
        k4 = interpolate3D3Dpoint(V,self.pos[-1]+self.h*k3)
        step = self.h/6*(k1 + 2*k2 + 2*k3 + k4)
        
        # Step all paths (with stochastic spread)
        self.pos.append(self.pos[-1] + step + spread*randn(3))
        for path in out:
            path.pos.append(path.pos[-1] + step + spread*randn(3))
        
        # Calculate probabilities of the new paths
        self.updateProb(P)
        for path in out:
            path.updateProb(P)
            
        # Return extra paths (current path was updated in place)
        return out
        
        
    def updateProb(self, P):
        
        p = 1.0
        
        # Get probability based on probablity mask (complex diff)
        p = p * interpolate3Dpoint(P,self.pos[-1])
        
        # Probabolity based on % change in KE
        if (len(self.pos) > 2):
            dv1 = self.pos[-2] - self.pos[-3]
            dv2 = self.pos[-1] - self.pos[-2]
            dKE = (dot(dv1,dv1)-dot(dv2,dv2))/dot(dv1,dv1)
            if (abs(dKE) > 1): dKE=1 # Is this too strict?
            p = p * (1-abs(dKE))
                
        self.plist.append(p)
        self.plist.popleft()
        
        self.prob = prod(self.plist)
            
        
    def display(self):
        patharray = array(self.pos)
        print(patharray)
        
    def plot(self, axes, crop=0.0):
        patharray = array(self.pos)
        plot(patharray[:,axes[0]]-crop,patharray[:,axes[1]]-crop)
        
def stepPaths(pathlist, V):
    h = pathlist[0].h
    print(h)
    pos0 = array([path.pos[-1] for path in pathlist])
    
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k1*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k2*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k3*h
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    step = h/6*(k1 + 2*k2 + 2*k3 + k4)
    
    for i in range(len(pathlist)):
        pathlist[i].pos.append(pathlist[i].pos[-1] + step[i,:])
        

def stepPathsDisplace(pathlist, V, offset):
    h = offset
    pos0 = array([path.pos[-1] for path in pathlist])
    
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k1*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k2*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k3*h
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    step = h/6*(k1 + 2*k2 + 2*k3 + k4)
    
    pos0 = pos0+step
    h = pathlist[0].h
    
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k1*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k2*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k3*h
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    step = h/6*(k1 + 2*k2 + 2*k3 + k4)
    
    for i in range(len(pathlist)):
        pathlist[i].pos.append(pathlist[i].pos[-1] + step[i,:])
        
def stepPathsDisplaceRand(pathlist, V, offset, P, spread, cutoff, reducer):
    h = offset
    print(h)
    
    start_length = len(pathlist)
    
    pos0 = array([path.pos[-1] for path in pathlist])
    
    toolow = nonzero(pos0<4)[0]
    toohigh = nonzero(pos0>315)[0]
    
    oobounds = unique(concatenate((toolow, toohigh)))
    pos0 = delete(pos0, oobounds, axis=0)
    oobounds = sort(oobounds)[::-1]
    
    print((len(oobounds)))
    
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k1*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k2*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k3*h
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    step = h/6*(k1 + 2*k2 + 2*k3 + k4)
    
    pos0 = pos0+step#+spread*randn(pos0.shape[0],pos0.shape[1])
    h = pathlist[0].h
    
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k1*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k2*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k3*h
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    step = h/6*(k1 + 2*k2 + 2*k3 + k4)
    
    for i in oobounds:
        pathlist.pop(i)
    
    kill_list = []
    for i in range(len(pathlist)):
        prob = 0
        tries = 0
        spreadi = spread
        cutoffi = cutoff
        while (prob < cutoffi):
            newpos = pathlist[i].pos[-1] + step[i,:] + spreadi*randn(3)
            prob = newStepProb(pathlist[i].pos, newpos, P)
            tries = tries + 1
            if tries == 30:
                cutoffi = cutoffi / reducer
                spreadi = spreadi*reducer
            if tries == 60:
                cutoffi = cutoffi / reducer
                spreadi = spreadi*reducer
            #if tries == 45:
            #    cutoffi = cutoffi / reducer
            #    spreadi = spreadi*reducer
            if tries > 90:
                kill_list.append(i)
                break
        pathlist[i].pos.append(newpos)
    
    kill_list.reverse()
    
    stoppedpaths = []
    for k in kill_list:
        #stoppedpaths.append(pathlist.pop(k))
        pathlist.pop(k)
    
    #getKE(pathlist)
    #pathlist.sort(key=operator.attrgetter('KE'))
    #crop0 = int(len(pathlist)*.1)
    #crop1 = int(len(pathlist)*.9)
    #del pathlist[:crop0]
    #del pathlist[crop1:]
    
    #Split the good lines further to keep up the number of lines
    N_new = start_length-len(pathlist)
    counter = 0
    while counter<N_new:
        ind = randint(low=0, high=len(pathlist))
        prob = 0
        tries = 0
        spreadi = spread
        cutoffi = cutoff
        while (prob < cutoffi):
            newpos = pathlist[ind].pos[-1] + spreadi*randn(3)
            prob = newStepProb(pathlist[ind].pos[:-1], newpos, P)
            tries = tries + 1
            if tries == 30:
                cutoffi = cutoffi / reducer
                spreadi = spreadi*reducer
            if tries == 60:
                cutoffi = cutoffi / reducer
                spreadi = spreadi*reducer
            #if tries == 45:
            #    cutoffi = cutoffi / reducer
            #    spreadi = spreadi*reducer
            if tries > 90:
                break
        if prob>cutoffi:
            pathlist.append(bPath(pathlist[ind].pos))
            pathlist[-1].pos[-1] = newpos
        counter = counter+1
 
    #return stoppedpaths

def getKE(pathlist):
    for path in pathlist:
        v = path.pos[-1] - path.pos[-2]
        path.KE = dot(v,v)
    
def stepPathsDisplaceRand2(pathlist, V, offset, P, spread, cutoff):
    h = offset
    print(h)
    pos0 = array([path.pos[-1] for path in pathlist])
    
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k1*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k2*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k3*h
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    step = h/6*(k1 + 2*k2 + 2*k3 + k4)
    
    pos0 = pos0+step
    h = pathlist[0].h
    
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k1*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k2*h/2
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    pos1 = pos0+k3*h
    
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    
    step = h/6*(k1 + 2*k2 + 2*k3 + k4)
    
    Nt = 5
    kill_list = []
    for i in range(len(pathlist)):
        probs = {}
        for t in range(Nt):
            newpos = pathlist[i].pos[-1] + step[i,:] + spread*randn(3)
            prob = newStepProb(pathlist[i].pos, newpos, P)
            probs[prob] = newpos
        pvals = sorted(probs.keys())
        maxprob = pvals[-1]
        if maxprob > cutoff:
            pathlist[i].pos.append(newpos)
        else:
            kill_list.append(i)
    
    kill_list.reverse()
    
    stoppedpaths = []
    for k in kill_list:
        stoppedpaths.append(pathlist.pop(k))
        
    return stoppedpaths

def newStepProb(pos, newpos, P):
    p = 1.0
        
    p = p * interpolate3Dpoint(P,newpos)
    
    # Probability based on % change in KE
    if (len(pos) > 1):
        dv1 = pos[-1] - pos[-2]
        dv2 = newpos - pos[-1]
        dKE = (dot(dv1,dv1)-dot(dv2,dv2))/dot(dv1,dv1)
        if (abs(dKE) > 1): dKE=1
        p = p * (1-abs(dKE))
            
    return p


def randomizeSplit(pathlist, P, split, spread):
    outlist = []
    for i in range(len(pathlist)):
        for j in range(split):
            outlist.append(bPath(pathlist[i].pos))
            outlist[-1].prob = pathlist[i].prob
            outlist[-1].plist = deque(pathlist[i].plist)
            outlist[-1].pos[-1] = outlist[-1].pos[-1] + spread*randn(3)
            outlist[-1].updateProb(P)
            
    return outlist
