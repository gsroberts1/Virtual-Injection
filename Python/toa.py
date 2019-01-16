from pylab import *
from interpolate_testcy import grid3Dpointarray

def TOAMap(pathlist, shape, scale = 1.0):
    A = zeros(shape)
    if (scale>20000.0): scale = 20000.0
    
    pos0 = array([path.pos[-1] for path in pathlist])
    
    r0 = floor(pos0)
    r1 = ceil(pos0)
    dr = pos0 - r0
    ddr = 1.0 - dr
    
    grid3Dpointarray(A,r0,r1,dr,ddr,scale)
    
    return A
        
def TOASmear(pathlist, shape):
    tmax = len(pathlist[0].pos)
    A = zeros(shape)
    for t in range(tmax):
        for path in pathlist:
            grid3Dpoint(A,path.pos[t],1.0)
    im = sum(A,axis=2)
    figure()
    imshow(im, origin='lower', vmax=4000)
    set_cmap('gray')
    colorbar()
    savefig('./GIF/%03d.png' % tmax)
            
        