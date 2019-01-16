from pylab import *
import os

fold = '/data/loecher/INJECT5/'

for i in range(19,799,20):
    ii = i-60

    if ii>499: ii = 499

    M0 = load(fold + 'TOAcar1_t%04d.npy' % i)
    M1 = load(fold + 'TOAcar2_t%04d.npy' % i)
    if ii > 0:
        M2 = load(fold + 'TOAbasi_t%04d.npy' % ii)
    else:
        M2 = zeros(M0.shape)
    
    for d in range(3):
        im = zeros((320,320,3))
        #im[:,:,0] = sum(M0,axis=d)[::-1,:]
        #im[:,:,1] = sum(M1,axis=d)[::-1,:]
        #im[:,:,2] = sum(M2,axis=d)[::-1,:]
        im[:,:,0] = M0.max(d)[::-1,:]
        im[:,:,1] = M1.max(d)[::-1,:]
        im[:,:,2] = M2.max(d)[::-1,:]
        
        
        im[im>350] = 350
        im = im/350
        
        savename = 'maxmultives_d%d_t%04d.png' % (d,i)
        
        figure()
        imshow(im, origin='lower')
        savefig(fold + savename)
        close()
        
        #imwhite = sum(im, axis=2)
        imwhite = im.max(2)
        
        savename = 'maxmultiveswh_d%d_t%04d.png' % (d,i)
        
        figure()
        imshow(imwhite, origin='lower', cmap='gray')
        savefig(fold + savename)
        close()
        
        print(savename)
    
#filelist = os.listdir(fold)
#
#for f in filelist:
#    if f[-4:]=='.npy' and f[:3]=='TOA':
#        M = load(fold + f)
#        for d in range(3):
#            savename = f[3:-4] + '_d%d.png' % d
#            if not os.path.exists(fold + savename):
#                print(savename)
#                im = sum(M,axis=d)
#                figure()
#                imshow(im, origin='lower', vmax=500)
#                set_cmap('gray')
#                colorbar()
#                savefig(fold + savename)
#                close()
                