import os
import numpy as np
import nibabel as nib
from nibabel.testing import data_path

test = np.load('D:\RECON_201810282230_mrflow\inject_data\TOAf1_t0029.npy')
img = nib.Nifti1Image(test, np.eye(4))
nib.save(img, os.path.join('build','test4d.nii.gz'))
