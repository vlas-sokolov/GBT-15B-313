#!/usr/bin/env python
import GAS_gridregion
import textwrap
import sys
import os
from astropy.io import fits

# TODO: restucture - make a __main__ block with following arguments:
#	- cloud
#	- do_sdfits
#	- do_calibration
#	- do_imaging
cloud = 'A'
from cloud_keys import keys
session = keys[cloud]['session'] 
source  = keys[cloud]['source' ] 
region  = keys[cloud]['region' ] 
windows = keys[cloud]['windows'] 
nblocks = keys[cloud]['nblocks']
scans   = keys[cloud]['scans'  ] 
gains   = keys[cloud]['gains'  ] 
windows = ['2'] # Only NHc(1,1) to test the system

# Re-generate sdfits files
import subprocess
assert type(scans) is list # better safe than sorry
scan_blocks = ','.join(['%i:%i'%(s['start'],s['end']) for s in scans])
sdfits_args = '-scans=\"%s\" %.2i' % (scan_blocks, session)
subprocess.Popen('sdfits-test -backends=vegasi AGBT15B_313_'+sdfits_args)

# Run the GAS pipeline wrapper
for window in windows:
	for block in range(nblocks):	
		GAS_gridregion.doPipeline(
		   SessionNumber = session,
	 	   StartScan     = scans[block]['start'],
		   EndScan       = scans[block]['end'  ], 
		   Source        = source,
		   Gains         = gains, 
		   Region        = region, 
		   Window        = str(window), 
		   overwrite     =True                    )

# I had to run this manually :S
#mv *window0*.fits cloudA_NH3_11/.
# TODO: a proper handling of directory struture

# Image the calibrated data
#data_dir='/lustre/pipeline/scratch/jpineda/Vlas/GBT-15B-313/'
data_dir='/lustre/pipeline/scratch/vsokolov/GBT-15B-313/'
startChannel, endChannel = 3200, 5000
file_extension='_test'
GAS_gridregion.griddata(rootdir=data_dir, 
                        region=Region, 
                        dirname=Region+'_NH3_11', 
                        startChannel = startChannel, 
                        endChannel = endChannel, 
                        #baselineRegion = [TODO],
                        file_extension=file_extension)
