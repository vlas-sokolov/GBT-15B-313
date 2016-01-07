#!/usr/bin/env python
#
# A master script for reducing GBT data. Intended to be run 
# from command line, but importing the file would load the
# "map_cloud" routine, which could be used directly. If
# called byexecfile, some sensible defaults are assumed.
#
# Example uses:
# - recalibrate cloud A data:
#   $ ./reduce.py --calib --sources A
# - do imaging only on clouds  A, J, and J:
#   $ python reduce.py --sources J A B
#
from cloud_keys import keys, WindowDict
from basemask import basebox, chanmin, chanmax

def main():
	# Setting up the command line interaction
	import argparse
	parser = argparse.ArgumentParser(description =
	                    'Runs the GAS pipeline on GBT-15B-313.')
	parser.add_argument('--sdfits', dest='do_sdfits', 
			    action='store_true', default=False, 
			    help='re-run sdfits on VEGAS data')
	parser.add_argument('--calib', dest='do_calibration', 
			   action='store_true', default=False, 
			   help='run gbtpipeline GAS wrapper?')
	parser.add_argument('--noimage', dest='no_imaging', 
			    action='store_true', default=False, 
			    help='do not grid data into images')
	parser.add_argument('--sources', action='store', nargs='+',
	                   help='source(s) for the pipeline to process')
	
	args = parser.parse_args()
	# so this is a bit ugly, but it still allows to
	# exectute the main() block through execfile(reduce.py)
	if args.sources is None:
		print parser.format_usage()
		print 'assuming sources A, B, E, I, J'
		print 'consider passing --sources X Y Z',
		print 'from the command line'
		args.sources = ['A','B','E','I','J']
	for cloud in args.sources:
		map_cloud(cloud=cloud, do_calibration=args.do_calibration,
		          do_sdfits=args.do_sdfits, 
		          do_imaging=not args.no_imaging)

def map_cloud(cloud, do_sdfits=False, do_calibration=False, do_imaging=True, keys=keys):
	source  = keys[cloud]['source' ] 
	region  = keys[cloud]['region' ] 
	windows = keys[cloud]['windows'] 
	nblocks = keys[cloud]['nblocks']
	scans   = keys[cloud]['scans'  ] 
	gains   = keys[cloud]['gains'  ] 
	beam    = keys[cloud]['beam'   ] 

	# TODO: make --windows (or better yet, --lines) an cmd argument
	# pulls all unique values from a dictionary of {'ifnum':'lineName', ...} form:
	lines = [] 
	_ = [(WindowDict[ifn],lines.append(WindowDict[ifn])) 
		for ifn in WindowDict if WindowDict[ifn] not in lines]
	# NOTE: "lines" list controls the imaging loop, 
	#	while "windows" list controls calibration!
	# TODO: resolve lines/windows ambiguity!

	# Convert VEGAS raw data to sdfits
	if do_sdfits:
		import subprocess
		assert type(scans) is list # better safe than sorry
		unique_sessions = set([s['session'] for s in scans])
		for session in unique_sessions:
			# all scan blocks within one session are 
			# parsed in a "s1:s2,s3:s4,..." format and
			# then sent to sdfits-test for data-crunching
			scan_blocks = ','.join(['%i:%i'%(s['start'],s['end']) 
					       for s in scans] 
					       if s['session'] is session)
			sdfits_dir = ' AGBT15B_313_%.2i' % session
			sdfits_args = ' -scans=\"%s\"' % scan_blocks
			# TODO: oops I also need to properly set the output dir!
			subprocess.Popen('sdfits-test -backends=vegasi'+
					 sdfits_args+sdfits_dir)

	# it's being quite slow on the import, moved inside the script	
	import GAS_gridregion
	data_dir='/lustre/pipeline/scratch/vsokolov/'
	# Run the GAS pipeline wrapper
	if do_calibration:
		for window in windows:
			# TODO: this is way too slow; gbtpipeline can accept
			# arguments like -m "50:60,80:90", rewrite the 
			# GAS wrapper to accept faster arguments
			for block in range(nblocks):	
				GAS_gridregion.doPipeline(
				   SessionNumber = scans[block]['session'],
			 	   StartScan     = scans[block]['start'],
				   EndScan       = scans[block]['end'  ], 
				   Source        = source,
				   Gains         = gains, 
				   Region        = region, 
				   Window        = str(window), 
				   OutputRoot    = data_dir+region+'/',
				   overwrite     = True                   )
	
	# Image the calibrated data
	if do_imaging:
		# TODO: trim and implement proper vlsr corrections
		# cloud 'I' had a somewhat mismatched vlsr
		startChannel, endChannel = (2800, 4600) \
			if cloud is 'I' else (3200, 5000)
		for line in lines:
			GAS_gridregion.griddata(rootdir=data_dir, 
			                        region=region, 
			                        indir=region+'_'+line, 
			                        outfile=region+'_'+line, 
			                        startChannel = startChannel, 
			                        endChannel = endChannel, 
			                        doBaseline = True,
						baselineRegion = 
							basebox(cloud, line)+
							startChannel,
						useBeam = beam,
						file_extension='')

if __name__ == "__main__":
	main()
