from pylab import *

for i in range(19,2000,20):
    print(i)
    M = load('/data/loecher/INJECT/TOAc5_t%03d.npy' % i)
    
    #im = M.max(1)
    im = sum(M,axis=1)
    figure()
    imshow(im, origin='lower', vmax=500)
    set_cmap('gray')
    colorbar()
    savefig('/data/loecher/INJECT/testc5_%03d.png' % i)
    close()