from pylab import *
from interpolate_testcy import *


def iDC(Vd, dt0, n_iter):
    # IDC Iterative displacement correction for correcting displaced velocities
    # See: Thunberg P, Wigstrom L, Ebbers T, Karlsson M. JMRI, 2002;16(5):591-597.

    xrange = arange(1, Vd.shape[0])
    yrange = arange(1, Vd.shape[1])
    zrange = arange(1, Vd.shape[2])
    sX, sY, sZ = meshgrid(xrange, yrange, zrange)  # mesh grids for all x,y,z points
    seeds = [concatenate(sX), concatenate(sY), concatenate(sZ)]  # make seed points at all voxels

    Vc = Vd  # make space for corrected velocities
    for j in range(n_iter):
        N = 3
        displaced = step_paths(Vc, dt0/N, seeds)  # displace from original seeds
        for n in range(N-1):
            displaced = step_paths(Vc, dt0/N, displaced)  # displace from original seeds
        Vc = interpolate3D3Dpointarray(Vd, displaced)  # get updated velocity from corrected velocity map
        Vc = reshape(Vc, size(Vd))  # reshape to image

    return Vc


def step_paths(V, h, streams):
    # Standard RK4 numerical integration
    k1 = interpolate3D3Dpointarray(V, streams)
    k2 = interpolate3D3Dpointarray(V, streams + k1 * h / 2)
    k3 = interpolate3D3Dpointarray(V, streams + k2 * h / 2)
    k4 = interpolate3D3Dpointarray(V, streams + k3 * h)
    displaced = streams + (k1 + 2 * k2 + 2 * k3 + k4) * h / 6
    return displaced