


ls -d *.fits > cubes

for line in `cat cubes`
do

         fits in=${line} op=xyin out=${line}.map
        #echo done
         puthd in=${line}/restfreq value=0.11156
        #echo puthd done
         maths exp="<${line}.map>" mask="<${line}.map>.ne.0" out=${line}.blank
         regrid in=${line}.blank out=${line}.rgd tin=new_1132158368_1132158488_1160cube_shifted.fits.blank
done



ls -d *.rgd > Corrected_Cubes_rgd

 imcomb in=@Corrected_Cubes_rgd out=Orion_I_${chan1}.map rms=@rms_full options=relax

 fits in=Orion_I_${chan1}.map out=Orion_I_${chan1}_Continuum.fits op=xyout

 imbin in=Orion_I_${chan1}.map out=Orion_I_${chan1}.bin bin=1,1,1,1,15,15

 regrid in=Orion_I_${chan1}.bin out=Orion_I_${chan1}.rgd tin=Orion_I_${chan1}.map

 maths exp='<Orion_I_1160.map>-<Orion_I_1160.rgd>' out=Orion_I_${chan1}Subtracted.map

 fits in=Orion_I_${chan1}Subtracted.map out=Orion_I_${chan1}_Subtracted.fits op=xyout

 puthd in=Orion_I_${chan1}Subtracted.map/restfreq value=0.105

 moment in=Orion_I_${chan1}Subtracted.map out=Orion_I_${chan1}Subtracted.moment mom=-2
