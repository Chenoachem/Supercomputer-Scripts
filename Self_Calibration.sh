#!/bin/bash -l

# Calibrate the data

#SBATCH --account=mwasci
#SBATCH --partition=longq
#SBATCH --time=24:00:00
#SBATCH --output=/astro/mwasci/ctremblay/Out_Files/self_1089030608.o%j
#SBATCH --error=/astro/mwasci/ctremblay/Out_Files/self_1089030608.e%j
#SBATCH --export=NONE

#aprun="aprun -n 1 -d 20 -q "
datadir=/astro/mwasci/ctremblay
proj=GC_RRL
obsnum=1089030608
ncpus=20
# you could modify the submission script and template to change these more dynamically:
imsize=4000
scale=0.0065

#cd /${datadir}/${proj}/${obsnum}/Calibrators
cd /astro/mwasci/ctremblay/GC_RRL/1089030608

flagantennae ${obsnum}.ms 52 55 74

# Initial clean to first negative
wsclean -name ${obsnum}_initial -size ${imsize} ${imsize} -scale ${scale} -abs-mem 50 -stopnegative -niter 400000 -threshold 0.01 -weight briggs -1.0  ${obsnum}.ms

# FT the Stokes I model into the visibilities
wsclean -predict -name ${obsnum}_initial -abs-mem 50 -size ${imsize} ${imsize} -pol I -weight briggs -1.0 -scale ${scale}  ${obsnum}.ms

# Calibrate: by default, it will use the MODEL column, which now has the FT'd self-cal model
calibrate -absmem 32 -minuv 20 ${obsnum}.ms ${obsnum}_self_solutions.bin
#calibrate -m ${modeldir}/${calmodel} -absmem 32 -minuv 20 ${obsnum}.ms ${obsnum}_${calnotxt}_solutions_Flagg.bin
# Apply the calibration solutions
applysolutions ${obsnum}.ms ${obsnum}_self_solutions.bin

#Make Test Images
time wsclean -name ${obsnum}_test -size ${imsize} ${imsize} -abs-mem 32 -niter 400000 -auto-threshold 5 -mgain 0.85 -weight briggs -1.0 -scale ${scale} -cleanborder 1 ${obsnum}.ms
