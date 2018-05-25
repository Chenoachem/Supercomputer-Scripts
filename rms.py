import astropy
from astropy.io import fits
from astropy.modeling import models
import numpy as np
import sys
import os.path

file1=sys.argv[1]

datacube = fits.open(file1)
data = datacube[0].data
header = datacube[0].header
cube = data[:,:,:]
rms_number = np.nanstd(cube[:,:,400:700,400:700])
print rms_number
#np.savetxt("rmsvals.txt", rmsval)
if os.path.exists('rms_full'):
    with open('rms_full', 'a') as f:
        f.write(str(rms_number)+"\n")
else:
    f = open('rms_full', 'w')
    f.write(str(rms_number)+"\n",'w')
