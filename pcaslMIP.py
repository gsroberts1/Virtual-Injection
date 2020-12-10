import numpy as np
import os
from pylab import *

filename = "/data/data_flow/HEAD_NECK/PATIENTS/ANEURYSM/130805_ANUR/PCASL_DYN/X_2_0.dat"

fd = open(filename, 'rb')
size = 320*320*320
dtype = 'h' #found with numpy.dtype('int16').char
data = np.fromfile(file=fd, dtype=np.float32).reshape((320,320,320))

figure()
imshow(data[:,:,:].max(2), origin='upper', interpolation='none', vmax=2.5)
set_cmap('gray')
colorbar()
savefig('/export/home/loecher/short2pcasl.png')
show()