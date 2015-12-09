
import GAS_gridregion
import textwrap
import sys
import os

from astropy.io import fits

# TODO: will be repeated, but everything except for LPCs should be ok

# Daisy scan numbers:
# 16:18,23:34 | mapped those with a wrong value of vlsr in source.cat (30 instead of 65.8 km/s)
# 70:81,84:86 | daisy scans at the end of the run, with corrected vlsr value

# don't use AIPS at all... it is really ugly!
gbt_dir='/lustre/pipeline/scratch/vsokolov'

# run the pipeline
#gbtpipeline --clobber -u tmb --window 2 -m "70:81,84:86" -f 0,1,3,4,5,6 -i /home/scratch/vsokolov/AGBT15B_313_03.raw.vegas

# The default gains should be 1's
# the gains derived from GAS on semester 15B are below, and they provide a good intrabeam calibration
# however, there could be a small global correction to get the amplitude calibration right.
#
Gains = '1,1,1,1,1,1,1,1,1,1,1,1,1,1'
GAS_Gains='0.883,0.858,0.885,0.847,0.847,0.855,0.746,0.731,0.986,0.768,0.647,0.522,0.894,1.109'

window=['0','1','2','3','4','5','6']
window=['0'] # Only NHc(1,1) to test the system
Region='cloudA'

for thisWindow in window:
	GAS_gridregion.doPipeline(SessionNumber=3, StartScan=70, EndScan=81, Source='EG28.67', 
		Gains=Gains, Region=Region, Window=str(thisWindow), overwrite=True)

	GAS_gridregion.doPipeline(SessionNumber=3, StartScan=84, EndScan=86, Source='EG28.67', 
		Gains=Gains, Region=Region, Window=str(thisWindow), overwrite=True)

# I had to run this manually :S
#mv *window0*.fits cloudA_NH3_11/.

data_dir='/lustre/pipeline/scratch/jpineda/Vlas/GBT-15B-313/'
startChannel = 1024 + 668 # default 1024
endChannel = 1024 + 1452  # default 3072
file_extension='_test'
GAS_gridregion.griddata( rootdir=data_dir, region=Region, 
        dirname=Region+'_NH3_11', 
        startChannel = startChannel, endChannel = endChannel, 
        file_extension=file_extension)