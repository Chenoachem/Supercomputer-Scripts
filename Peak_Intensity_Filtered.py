#!/usr/bin/python

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

mycube=sys.argv[1]
cat_files = sys.argv[2]

#Open the cube in which the search was done on
datacube = fits.open(mycube)
data = datacube[0].data
header = datacube[0].header

#Make a list of all the frequencies for all the channels in the cube.  Convert those to MHz.
rp = datacube[0].header['CRPIX3']
rf = datacube[0].header['CRVAL3']
df = datacube[0].header['CDELT3']
nf = datacube[0].header['NAXIS3']
xvals = rf + df*(np.arange(nf)-rp)
xvals=xvals*10**-6

#For each pixel location in the catalogue file, convert the coordinates to pixel coordinates, check the spectral RMS and local RMS
#Filter the results based on SNR and RMS.  For those that pass criteria, make a spectra.

file=open(cat_files)
for line in file:
    ra,dec = line.strip().split(",")
    ra=str(ra)
    dec=str(dec)
    c = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))

    w = wcs.WCS(header, naxis=2)

    xpix,ypix=c.to_pixel(w,origin=0,mode='wcs')    
    xpix=int(xpix)
    ypix=int(ypix)

    signal=[]
    for x in range(0, 100):
        value = np.mean(data[:,x,ypix:ypix+1,xpix:xpix+1])
        #print rms_number_x
        signal.append(value)
    
    max_signal=np.nan_to_num(signal)
    max_value = np.amax(max_signal)

    RMS=np.nanstd(signal)
    RMS2=str(round(RMS,2))

    snr=np.divide(max_value,RMS)

    slice=np.argmax(max_signal, axis=0)
    rms_number = np.nanstd(data[:,slice,ypix+5:ypix+15,xpix+5:xpix+15])

    if RMS<0.5 and snr>4 and rms_number<0.6:
        with open('ra_dec_cat2', 'a') as f:
            f.write(str(ra)+","+str(dec)+"\n")

        #Make a spectra

    	bigfig=plt.figure(figsize=(20,12))
    	ax1=bigfig.add_subplot(111)
    	ax1.step(xvals,signal,color='blue')
    	ax1.set_title("Orion Nebula "+"Signal Max: "+str(round(max_value,2))+"Frequency: "+str(round(xvals[slice],2))+"Spectral RMS: "+RMS2+" Local RMS: "+str(round(rms_number,2)),fontsize=18)
    	ax1.set_xlabel("Frequency (MHz)",fontsize=18)
    	ax1.set_ylabel("Flux Density (Jy/beam)",fontsize=18)
    	ax1.tick_params(labelsize=15)
      
    	bigfig.savefig("Orion_"+str(ra)+"_"+str(round(xvals[0],0))+"_.png")
