from pylab import *
import os

fold = './inject_data/'

filelist = os.listdir(fold)

for f in filelist:
    if f[-4:]=='.npy' and f[:3]=='TOA':
        check = 0
        for d in range(3):
            savename = f[3:-4] + '_d%d.png' % d
            if os.path.exists(fold + savename):
                check = check+1
        if check<3:
            M = load(fold + f)
            M[254:,:,:] = 0.0
            for d in range(3):
                savename = f[3:-4] + '_d%d.png' % d
                if not os.path.exists(fold + savename):
                    print(savename)
                    #im = sum(M,axis=d)
                    im = M.max(d)[::-1,:]
                    figure()
                    imshow(im, origin='lower', vmax=300)
                    set_cmap('gray')
                    colorbar()
                    savefig(fold + savename)
                    close()
                    
                    savename = f[3:-4] + '_sqrt_d%d.png' % d
                    im=sqrt(im)
                    figure()
                    imshow(im, origin='lower', vmax=25)
                    set_cmap('gray')
                    colorbar()
                    savefig(fold + savename)
                    close()
            
