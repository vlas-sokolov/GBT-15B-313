#!/usr/bin/env python
import GAS_gridregion
import textwrap
import sys
import os
from astropy.io import fits

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

data_dir='/lustre/pipeline/scratch/vsokolov/GBT-15B-313/'
#data_dir='/lustre/pipeline/scratch/jpineda/Vlas/GBT-15B-313/'
startChannel, endChannel = 3200, 5000

file_extension='_test'
GAS_gridregion.griddata( rootdir=data_dir, region=Region, 
        dirname=Region+'_NH3_11', 
        startChannel = startChannel, endChannel = endChannel, 
        file_extension=file_extension,
	#baselineRegion = [TODO]
	)
