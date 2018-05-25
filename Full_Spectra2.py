#!/usr/bin/python

import os
import numpy as np
import astropy
from astropy.io import fits
from astropy.coordinates import SkyCoord  # High-level coordinates
from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
from astropy.coordinates import Angle, Latitude, Longitude  # Angles
import astropy.units as u
from astropy import wcs
import sys
import os.path
import csv

#Code inputs

mycube=sys.argv[1]
ra = sys.argv[2]
dec = sys.argv[3]
outfile=sys.argv[4]

#Open fits file
datacube = fits.open(mycube)
data = datacube[0].data
header = datacube[0].header

#Convert the wcs coordinates to pixel coordinates
ra=str(ra)
dec=str(dec)
c = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))

w = wcs.WCS(header, naxis=2)

xpix,ypix=c.to_pixel(w,origin=0,mode='wcs')    
xpix=int(xpix)
ypix=int(ypix)

#create a list of frequencies within the cube
rp = datacube[0].header['CRPIX3']
rf = datacube[0].header['CRVAL3']
df = datacube[0].header['CDELT3']
nf = datacube[0].header['NAXIS3']
xvals = rf + df*(np.arange(nf)-rp)
xvals=xvals*10**-6

#Create a list of signal values for each channel within the cube at the ra and dec positions
signal=[]
for x in range(0, 100):
    #rms_number = np.nanstd(data[:,x,ypix+5:ypix+15,xpix+5:xpix+15])
    #if rms_number <30:
    value = np.mean(data[:,x,ypix:ypix+1,xpix:xpix+1])
    #else:
    #    value = np.nan
    signal.append(value)

#reformat the two list to have 2 decimal places
xvals_form = [ '%.2f' % elem for elem in xvals ]
signal_form = [ '%.2f' % elem for elem in signal ]

#join the two lists in pairs
zip(xvals_form,signal_form)

#if a file exists then append the data, if not then create and add the data
if os.path.isfile(outfile) == False:
    with open(outfile, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(zip(xvals_form,signal_form))
else:
    with open(outfile, 'a') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(zip(xvals_form,signal_form))






