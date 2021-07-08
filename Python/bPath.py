from pylab import *
from interpolate_testcy import *
from collections import deque


class bPath:
    def __init__(self, initPath):
        self.pos = list(initPath)
        self.prob = 1.0
        self.h = 2.0
        self.KE = 1.0
        self.plength = 4
        self.plist = deque([1.0, ] * self.plength)

    # ## TEST
    # def stepAlong(self, V, P, Split=0, spread=0.1):
    #     # Copy extra probabalistic paths
    #     out = []
    #     for i in range(Split):
    #         out.append(bPath(self.pos))
    #         out[i].prob = self.prob
    #         out[i].plist = deque(self.plist)
    #
    #     # Calculate deterministic step
    #     k1 = interpolate3D3Dpoint(V, self.pos[-1])
    #     k2 = interpolate3D3Dpoint(V, self.pos[-1] + self.h / 2 * k1)
    #     k3 = interpolate3D3Dpoint(V, self.pos[-1] + self.h / 2 * k2)
    #     k4 = interpolate3D3Dpoint(V, self.pos[-1] + self.h * k3)
    #     Step = self.h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    #
    #     # Step all paths (with stochastic spread)
    #     self.pos.append(self.pos[-1] + Step + spread * randn(3))
    #     for Path in out:
    #         Path.pos.append(Path.pos[-1] + Step + spread * randn(3))
    #
    #     # Calculate probabilities of the new paths
    #     self.updateProb(P)
    #     for Path in out:
    #         Path.updateProb(P)
    #
    #     # Return extra paths (current path was updated in place)
    #     return out
    #
    # ## TEST
    # def updateProb(self, P):
    #     p = 1.0
    #
    #     # Get probability based on probablity mask (complex diff)
    #     p = p * interpolate3Dpoint(P, self.pos[-1])
    #
    #     # Probabolity based on % change in KE
    #     if len(self.pos) > 2:
    #         dv1 = self.pos[-2] - self.pos[-3]
    #         dv2 = self.pos[-1] - self.pos[-2]
    #         dKE = (dot(dv1, dv1) - dot(dv2, dv2)) / dot(dv1, dv1)
    #         if abs(dKE) > 1:
    #             dKE = 1  # Is this too strict?
    #         p = p * (1 - abs(dKE))
    #
    #     self.plist.append(p)
    #     self.plist.popleft()
    #
    #     self.prob = prod(self.plist)
    #
    # ## TEST
    # def display(self):
    #     patharray = array(self.pos)
    #     print(patharray)
    #
    # ## TEST
    # def plot(self, axes, crop=0.0):
    #     patharray = array(self.pos)
    #     plot(patharray[:, axes[0]] - crop, patharray[:, axes[1]] - crop)


## No displacement correction
def stepPaths(pathlist, V):
    h = pathlist[0].h

    pos0 = array([path.pos[-1] for path in pathlist])
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k1 * h / 2
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k2 * h / 2
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k3 * h
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    Step = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    for i in range(len(pathlist)):
        pathlist[i].pos.append(pathlist[i].pos[-1] + Step[i, :])


## Single-step displacement correction (ssDC)
def stepPathsDisplace(pathlist, V, offset):
    h = offset
    pos0 = array([path.pos[-1] for path in pathlist])

    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k1 * h / 2
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k2 * h / 2
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos2 = pos0 + k3 * h
    r0 = floor(pos2)
    r1 = ceil(pos2)
    dr = pos2 - r0
    ddr = 1.0 - dr
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    Step = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    pos0 = pos0 + Step
    h = pathlist[0].h

    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k1 * h / 2
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k2 * h / 2
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos2 = pos0 + k3 * h
    r0 = floor(pos2)
    r1 = ceil(pos2)
    dr = pos2 - r0
    ddr = 1.0 - dr
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    Step = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    for i in range(len(pathlist)):
        pathlist[i].pos.append(pathlist[i].pos[-1] + Step[i, :])


## No displacement correction
def stepPathsRandConstr(pathlist, V, P, spread, cutoff, reducer, PLoader):
    h = pathlist[0].h
    start_length = len(pathlist)  # should be same as max_paths
    pos0 = array([path.pos[-1] for path in pathlist])

    maxRes = max(PLoader.resX, PLoader.resY, PLoader.resZ)
    toolow = nonzero(pos0 < 4)[0]
    toohigh = nonzero(pos0 > (maxRes - 5))[0]

    oobounds = unique(concatenate((toolow, toohigh)))
    pos0 = delete(pos0, oobounds, axis=0)
    oobounds = sort(oobounds)[::-1]
    print('# discarded: ' + str(len(oobounds)))

    ## Begin Runge-Kutta (RK4) Method
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    pos1 = pos0 + k1 * h / 2

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    pos1 = pos0 + k2 * h / 2

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    pos1 = pos0 + k3 * h

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    Step = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    for i in oobounds:
        pathlist.pop(i)

    kill_list = []
    for i in range(len(pathlist)):
        prob = 0
        tries = 0
        spreadi = spread
        cutoffi = cutoff
        while prob < cutoffi:
            newpos = pathlist[i].pos[-1] + Step[i, :] + spreadi * randn(3)
            prob = newStepProb(pathlist[i].pos, newpos, P)
            tries = tries + 1
            if tries == 30:
                cutoffi = cutoffi / reducer
                spreadi = spreadi * reducer
            if tries == 60:
                cutoffi = cutoffi / reducer
                spreadi = spreadi * reducer
            if tries > 90:
                kill_list.append(i)
                break
        pathlist[i].pos.append(newpos)

    kill_list.reverse()

    # stoppedpaths = []
    for k in kill_list:
        # stoppedpaths.append(pathlist.pop(k))
        pathlist.pop(k)

    # getKE(pathlist)
    # pathlist.sort(key=operator.attrgetter('KE'))
    # crop0 = int(len(pathlist)*.1)
    # crop1 = int(len(pathlist)*.9)
    # del pathlist[:crop0]
    # del pathlist[crop1:]

    # Add lost lines to keep up the number of lines
    N_new = start_length - len(pathlist)
    counter = 0
    while counter < N_new:
        ind = randint(low=0, high=len(pathlist))
        prob = 0
        tries = 0
        spreadi = spread
        cutoffi = cutoff
        while prob < cutoffi:
            newpos = pathlist[ind].pos[-1] + spreadi * randn(3)
            prob = newStepProb(pathlist[ind].pos[:-1], newpos, P)
            tries = tries + 1
            if tries == 30:
                cutoffi = cutoffi / reducer
                spreadi = spreadi * reducer
            if tries == 60:
                cutoffi = cutoffi / reducer
                spreadi = spreadi * reducer
            if tries > 90:
                break
        if prob > cutoffi:
            pathlist.append(bPath(pathlist[ind].pos))
            pathlist[-1].pos[-1] = newpos
        counter = counter + 1

    # return stoppedpaths

## Single-step displacement correction (ssDC) + Probalistic Streamlines
def stepPathsRand(pathlist, V, offset, spread, PLoader):
    h = offset  # temporal step size
    start_length = len(pathlist)  # should be same as max_paths
    pos0 = array([path.pos[-1] for path in pathlist])

    maxRes = max(PLoader.resX, PLoader.resY, PLoader.resZ)
    toolow = nonzero(pos0 < 4)[0]
    toohigh = nonzero(pos0 > (maxRes - 5))[0]

    oobounds = unique(concatenate((toolow, toohigh)))
    pos0 = delete(pos0, oobounds, axis=0)
    oobounds = sort(oobounds)[::-1]
    print('# discarded: ' + str(len(oobounds)))

    ## Begin Runge-Kutta (RK4) Method
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    pos1 = pos0 + k1 * h / 2

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    pos1 = pos0 + k2 * h / 2

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    pos1 = pos0 + k3 * h

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    Step = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    for i in oobounds:
        pathlist.pop(i)

    for i in range(len(pathlist)):
        newpos = pathlist[i].pos[-1] + Step[i, :] + spread * randn(3)
        pathlist[i].pos.append(newpos)


## Single-step displacement correction (ssDC) + Probalistic Streamlines
def stepPathsDisplaceRand(pathlist, V, offset, spread, PLoader):
    h = offset  # temporal step size
    start_length = len(pathlist)  # should be same as max_paths
    pos0 = array([path.pos[-1] for path in pathlist])

    maxRes = max(PLoader.resX, PLoader.resY, PLoader.resZ)
    toolow = nonzero(pos0 < 4)[0]
    toohigh = nonzero(pos0 > (maxRes - 5))[0]

    oobounds = unique(concatenate((toolow, toohigh)))
    pos0 = delete(pos0, oobounds, axis=0)
    oobounds = sort(oobounds)[::-1]
    print('# discarded: ' + str(len(oobounds)))

    ## Begin Runge-Kutta (RK4) Method
    r0 = floor(pos0)  # left endpoint for interp
    r1 = ceil(pos0)  # right endpoint for interp
    dr = pos0 - r0  # get distance from left endpoint to true point (for interpolation)
    ddr = 1.0 - dr  # get distance from right endpoint
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)  # get interp velocity (dr/dt=k1) at pos0

    pos1 = pos0 + k1 * h / 2  # move to midpoint (h/2) using slope k1
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)  # get interpolated velocity at first pos1

    pos1 = pos0 + k2 * h / 2  # move to midpoint (h/2) using slope k2
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)  # get interpolated velocity at second pos1

    pos2 = pos0 + k3 * h  # move to endpoint (h) using slope k3
    r0 = floor(pos2)
    r1 = ceil(pos2)
    dr = pos2 - r0
    ddr = 1.0 - dr
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)  # get interpolated velocity at pos2

    Step = h / 6 * (
                k1 + 2 * k2 + 2 * k3 + k4)  # get approximation of velocity trajectory (weighted average of dr/dt's)
    pos0 = pos0 + Step  # Move along v
    h = pathlist[0].h

    ## Perform second RK4 step
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    pos1 = pos0 + k1 * h / 2

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    pos1 = pos0 + k2 * h / 2

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    pos1 = pos0 + k3 * h

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    Step = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


    for i in oobounds:
        pathlist.pop(i)

    for i in range(len(pathlist)):
        newpos = pathlist[i].pos[-1] + Step[i, :] + spread * randn(3)
        pathlist[i].pos.append(newpos)


## Single-step displacement correction (ssDC) + Probalistic Streamlines + Constraints
def stepPathsDisplaceRandConstr(pathlist, V, offset, P, spread, cutoff, reducer, PLoader):
    h = offset  # temporal step size
    start_length = len(pathlist)  # should be same as max_paths
    pos0 = array([path.pos[-1] for path in pathlist])

    maxRes = max(PLoader.resX, PLoader.resY, PLoader.resZ)
    toolow = nonzero(pos0 < 4)[0]
    toohigh = nonzero(pos0 > (maxRes - 5))[0]

    oobounds = unique(concatenate((toolow, toohigh)))
    pos0 = delete(pos0, oobounds, axis=0)
    oobounds = sort(oobounds)[::-1]
    print('# discarded: ' + str(len(oobounds)))

    ## Begin Runge-Kutta (RK4) Method
    r0 = floor(pos0)  # left endpoint for interp
    r1 = ceil(pos0)  # right endpoint for interp
    dr = pos0 - r0  # get distance from left endpoint to true point (for interpolation)
    ddr = 1.0 - dr  # get distance from right endpoint
    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)  # get interp velocity (dr/dt=k1) at pos0

    pos1 = pos0 + k1 * h / 2  # move to midpoint (h/2) using slope k1
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)  # get interpolated velocity at first pos1

    pos1 = pos0 + k2 * h / 2  # move to midpoint (h/2) using slope k2
    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr
    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)  # get interpolated velocity at second pos1

    pos2 = pos0 + k3 * h  # move to endpoint (h) using slope k3
    r0 = floor(pos2)
    r1 = ceil(pos2)
    dr = pos2 - r0
    ddr = 1.0 - dr
    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)  # get interpolated velocity at pos2

    Step = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)  # approximation of velocity trajectory (weighted average of dr/dt's)
    # pos0 = pos0 + Step  # Move along v
    # h = pathlist[0].h
    #
    # ## Perform second RK4 step
    # r0 = floor(pos0)
    # r1 = ceil(pos0)
    # dr = pos0 - r0
    # ddr = 1.0 - dr
    # k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    # pos1 = pos0 + k1 * h / 2
    #
    # r0 = floor(pos1)
    # r1 = ceil(pos1)
    # dr = pos1 - r0
    # ddr = 1.0 - dr
    # k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    # pos1 = pos0 + k2 * h / 2
    #
    # r0 = floor(pos1)
    # r1 = ceil(pos1)
    # dr = pos1 - r0
    # ddr = 1.0 - dr
    # k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    # pos1 = pos0 + k3 * h
    #
    # r0 = floor(pos1)
    # r1 = ceil(pos1)
    # dr = pos1 - r0
    # ddr = 1.0 - dr
    # k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)
    #
    # Step = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    for i in oobounds:
        pathlist.pop(i)

    kill_list = []
    for i in range(len(pathlist)):
        prob = 0
        tries = 0
        spreadi = spread
        cutoffi = cutoff
        while prob < cutoffi:
            newpos = pathlist[i].pos[-1] + Step[i, :] + spreadi * randn(3)
            prob = newStepProb(pathlist[i].pos, newpos, P)
            tries = tries + 1
            if tries == 30:
                cutoffi = cutoffi / reducer
                spreadi = spreadi * reducer
            if tries == 60:
                cutoffi = cutoffi / reducer
                spreadi = spreadi * reducer
            if tries > 90:
                kill_list.append(i)
                break
        pathlist[i].pos.append(newpos)

    kill_list.reverse()

    # stoppedpaths = []
    for k in kill_list:
        # stoppedpaths.append(pathlist.pop(k))
        pathlist.pop(k)

    # getKE(pathlist)
    # pathlist.sort(key=operator.attrgetter('KE'))
    # crop0 = int(len(pathlist)*.1)
    # crop1 = int(len(pathlist)*.9)
    # del pathlist[:crop0]
    # del pathlist[crop1:]

    # Add lost lines to keep up the number of lines
    # N_new = start_length - len(pathlist)
    # counter = 0
    # while counter < N_new:
    #     ind = randint(low=0, high=len(pathlist))
    #     prob = 0
    #     tries = 0
    #     spreadi = spread
    #     cutoffi = cutoff
    #     while prob < cutoffi:
    #         newpos = pathlist[ind].pos[-1] + spreadi * randn(3)
    #         prob = newStepProb(pathlist[ind].pos[:-1], newpos, P)
    #         tries = tries + 1
    #         if tries == 30:
    #             cutoffi = cutoffi / reducer
    #             spreadi = spreadi * reducer
    #         if tries == 60:
    #             cutoffi = cutoffi / reducer
    #             spreadi = spreadi * reducer
    #         if tries > 90:
    #             break
    #     if prob > cutoffi:
    #         pathlist.append(bPath(pathlist[ind].pos))
    #         pathlist[-1].pos[-1] = newpos
    #     counter = counter + 1

    # return stoppedpaths


def getKE(pathlist):
    for path in pathlist:
        v = path.pos[-1] - path.pos[-2]
        path.KE = dot(v, v)


def stepPathsDisplaceRand2(pathlist, V, offset, P, spread, cutoff):
    h = offset  # temporal step size
    print(h)
    pos0 = array([path.pos[-1] for path in pathlist])

    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr

    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k1 * h / 2

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr

    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k2 * h / 2

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr

    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k3 * h

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr

    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    Step = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    pos0 = pos0 + Step
    h = pathlist[0].h

    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr

    k1 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k1 * h / 2

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr

    k2 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k2 * h / 2

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr

    k3 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    pos1 = pos0 + k3 * h

    r0 = floor(pos1)
    r1 = ceil(pos1)
    dr = pos1 - r0
    ddr = 1.0 - dr

    k4 = interpolate3D3Dpointarray(V, r0, r1, dr, ddr)

    Step = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    Nt = 5
    kill_list = []
    for i in range(len(pathlist)):
        probs = {}
        for t in range(Nt):
            newpos = pathlist[i].pos[-1] + Step[i, :] + spread * randn(3)
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
    p = p * interpolate3Dpoint(P, newpos)

    # Probability based on % change in KE=1/2mV^2=1/2m|dx/dt|^2
    if len(pos) > 1:
        dv1 = pos[-1] - pos[-2]  # labelled dv not dx because dt will cancel out below
        dv2 = newpos - pos[-1]
        dKE = (dot(dv1, dv1) - dot(dv2, dv2)) / dot(dv1, dv1)  # normalized change in KE
        # m, dt, 1/2's cancel out, leaving only dx; dKE=1-(dv2/dv1)^2
        if abs(dKE) > 1:  # consider making denominator of dKE = (dot(dv1, dv1) + dot(dv2, dv2))
            dKE = 1
        p = p * (1 - abs(dKE))

    return p


def randomizeSplit(pathlist, P, Split, spread):
    outlist = []
    for i in range(len(pathlist)):
        for j in range(Split):
            outlist.append(bPath(pathlist[i].pos))
            outlist[-1].prob = pathlist[i].prob
            outlist[-1].plist = deque(pathlist[i].plist)
            outlist[-1].pos[-1] = outlist[-1].pos[-1] + spread * randn(3)
            outlist[-1].updateProb(P)

    return outlist
