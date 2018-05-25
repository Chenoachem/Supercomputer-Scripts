
#!/bin/python

import os
import argparse
import numpy as np
import astropy
from astropy.io import fits
import matplotlib
from matplotlib import pyplot as plt
from astropy.coordinates import SkyCoord  # High-level coordinates
from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
from astropy.coordinates import Angle, Latitude, Longitude  # Angles
import astropy.units as u
from astropy import wcs
import math
import sys

snr_cube=sys.argv[1]
freq=sys.argv[2]


datacube = fits.open(snr_cube)
data = datacube[0].data
header = datacube[0].header
cube = data[:,:,:]

#Determine the list of frequencies in the cube
rp = datacube[0].header['CRPIX3']
rf = datacube[0].header['CRVAL3']
df = datacube[0].header['CDELT3']
nf = datacube[0].header['NAXIS3']
xvals = rf + df*(np.arange(nf)-rp)
xvals_small=xvals[0:100]/10**6

#Find the right slice for the given frequency
freq=float(freq)
slice=np.where(xvals_small==freq)

rms_number = np.nanstd(cube[:,slice,1400:1700,1400:1700])
print rms_number

#Create the two histograms
counts,bins = np.histogram(cube[:,slice,1400:1700,1400:1700],bins=np.arange(-5,5,0.2))
fig2=plt.figure()

my_suptitle = plt.suptitle("Pixel Histogram 1399:1700 - Slice" + str(slice[0])+ " Frequency "+ str(freq), y=1.08)

ax=fig2.add_subplot(1,2,1)
ax.semilogy(bins[:-1],counts)
ax.set_title("Log Plot")
ax.set_xlim([-4,4])

ax2=fig2.add_subplot(1,2,2)
ax2.plot(bins[:-1],counts)
ax2.set_xlim([-4,4])
ax2.set_title("Normal Histogram")

#plt.suptitle("Pixel Histogram 1399:1700 - Slice" + str(slice[0])+ " Frequency "+ str(freq), y=1.08) 
plt.tight_layout(pad=0.7)


fig2.savefig('Histogram_Subtracted_'+str(round(freq,2))+'.png', bbox_inches='tight',bbox_extra_artists=[my_suptitle])






