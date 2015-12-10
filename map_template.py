#!/usr/bin/env python
#
# A master script for reducing GBT data. Intended to be run 
# from command line, but importing the file would load the
# "map_cloud" routine, which could be used directly. If an
# execfile is called it, some sensible defaults are assumed.
#
# Example uses:
# - recalibrate cloud A data:
#   $ ./map_template.py --calib --source A
# - do imaging only on clouds  A, J, and J:
#   $ python map_template.py --source J A B
#
from cloud_keys import keys

data_dir='/lustre/pipeline/scratch/vsokolov/GBT-15B-313/'

def main():
	# Setting up the command line interaction
	import argparse
	parser = argparse.ArgumentParser(description =
	                    'Runs the GAS pipeline on GBT-15B-313.')
	parser.add_argument('--sdfits', dest='do_sdfits', 
			    action='store_false', default=False, 
			    help='re-run sdfits on VEGAS data')
	parser.add_argument('--calib', dest='do_calibration', 
			   action='store_false', default=False, 
			   help='run gbtpipeline GAS wrapper?')
	parser.add_argument('--noimage', dest='no_imaging', 
			    action='store_true', default=False, 
			    help='do not grid data into images')
	parser.add_argument('--source', action='store', nargs='+',
	                   help='source(s) for the pipeline to process')
	
	args = parser.parse_args()
	# so this is a bit ugly, but it still allows to
	# exectute the main() block through execfile(map_template.py)
	if args.source is None:
		print parser.format_usage()
		print 'assuming sources A, B, E, I, J'
		print 'consider passing --source X Y Z',
		print 'from the command line'
		args.source = ['A','B','E','I','J']

	for cloud in args.source:
		map_cloud(cloud=cloud, do_calibraion=args.do_calibration,
		          do_sdfits=args.do_sdfits, 
		          do_imaging=not args.no_imaging)

def map_cloud(cloud, do_sdfits=False, do_calibration=False, do_imaging=True, keys=keys):
	session = keys[cloud]['session'] 
	source  = keys[cloud]['source' ] 
	region  = keys[cloud]['region' ] 
	windows = keys[cloud]['windows'] 
	nblocks = keys[cloud]['nblocks']
	scans   = keys[cloud]['scans'  ] 
	gains   = keys[cloud]['gains'  ] 
	windows = ['2'] # Only NHc(1,1) to test the system
	
	# Convert VEGAS raw data to sdfits
	if do_sdfits:
		import subprocess
		assert type(scans) is list # better safe than sorry
		scan_blocks = ','.join(['%i:%i'%(s['start'],s['end']) 
				       for s in scans])
		sdfits_dir = ' AGBT15B_313_%.2i' % session
		sdfits_args = ' -scans=\"%s\"' % scan_blocks
		subprocess.Popen('sdfits-test -backends=vegasi'+
				 sdfits_args+sdfits_dir)

	# it's being quite slow on the import, moved inside the script	
	import GAS_gridregion
	# Run the GAS pipeline wrapper
	if do_calibration:
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
	startChannel, endChannel = 3200, 5000
	file_extension='_test'
	GAS_gridregion.griddata(rootdir=data_dir, 
	                        region=Region, 
	                        dirname=Region+'_NH3_11', 
	                        startChannel = startChannel, 
	                        endChannel = endChannel, 
	                        #baselineRegion = [TODO],
	                        file_extension=file_extension)

if __name__ == "__main__":
	main()
