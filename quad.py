#!/usr/bin/env python

# Sum the squares one fits file to another

import sys

# fits files
try:
   import astropy.io.fits as fits
except ImportError:
   import pyfits as fits

file1=sys.argv[1]
file2=sys.argv[2]
output=sys.argv[3]

print "Summing "+file1+" and "+file2

hdu1=fits.open(file1)
hdu2=fits.open(file2)
hdu1[0].data=(hdu1[0].data + hdu2[0].data)/2
hdu1.writeto(output,clobber=True)
