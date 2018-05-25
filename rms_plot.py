import astropy
from astropy.io import fits
from astropy.modeling import models
import numpy as np
import sys
import numpy as np
import matplotlib.pyplot as plt

cube=sys.argv[1]

datacube = fits.open(cube)
data = datacube[0].data
header = datacube[0].header
cube = data[:,:,:]

number_list=[]

for x in range(6, 95):
    rms_number_x = np.nanstd(cube[:,x:x+1,400:700,400:700])
    #print rms_number_x
    number_list.append(rms_number_x)


plt.plot(number_list, "r-")
plt.title("RMS per slice")

plt.savefig("rms_cube_plot.png")
