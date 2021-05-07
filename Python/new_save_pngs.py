from pylab import *
from tkinter import filedialog
import os

#fold = './inject_data/'

fold = filedialog.askdirectory()
fold = fold + '/'
filelist = os.listdir(fold)

try:
    os.mkdir(fold + 'raw')
except FileExistsError:
    pass

try:
    os.mkdir(fold + 'sqrt')
except FileExistsError:
    pass


try:
    os.mkdir(fold + 'raw/ax')
except FileExistsError:
    pass

try:
    os.mkdir(fold + 'raw/cor')
except FileExistsError:
    pass


try:
    os.mkdir(fold + 'raw/sag')
except FileExistsError:
    pass

try:
    os.mkdir(fold + 'sqrt/ax')
except FileExistsError:
    pass


try:
    os.mkdir(fold + 'sqrt/cor')
except FileExistsError:
    pass

try:
    os.mkdir(fold + 'sqrt/sag')
except FileExistsError:
    pass


# d0 = axial
# d1 = coronal
# d2 = sagittal
for f in filelist:
    if f[-4:]=='.npy' and f[:3]=='TOA':
        check = 0
        for d in range(3):
            savename = f[3:-4] + '_d%d.png' % d
            if os.path.exists(fold + savename):
                check = check+1
        if check<3:
            M = load(fold + f)
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
                    if d==1:
                        savefig(fold + 'raw/ax/' + savename)
                    elif d==2:
                        savefig(fold + 'raw/cor/' + savename)
                    else:
                        savefig(fold + 'raw/sag/' + savename)
                    close()
                    
                    savename = f[3:-4] + '_sqrt_d%d.png' % d
                    im=sqrt(im)
                    figure()
                    imshow(im, origin='lower', vmax=25)
                    set_cmap('gray')
                    colorbar()
                    if d==1:
                        savefig(fold + 'sqrt/ax/' + savename)
                    elif d==2:
                        savefig(fold + 'sqrt/cor/' + savename)
                    else:
                        savefig(fold + 'sqrt/sag/' + savename)
                    close()
            
