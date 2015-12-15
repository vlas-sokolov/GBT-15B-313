#!/usr/bin/env python
#
# A master script for post-processing calibrated GBT data. 
# Intended to be run from command line, but importing the 
# file would load the "firstlook" routine, which could be 
# used directly. If called by execfile, some sensible 
# defaults will be assumed.
#
# Available arguments:
# --firstlook: adapted from GAS* first_look routine,
#              does baseline fitting, rms estimates,
#              and performs moment analysis
# --cubefit  : fits ammonia, and, potentially, other 
#              line profiles to the spectral cubes;
#              Adapted from PropertyMaps.py @ GAS*.
# *GBT Ammonia Survey (https://github.com/GBTAmmoniaSurvey/GAS)
#
# Example uses:
# $ ./process.py --firstlook --sources A --lines HC5N
# $ python process.py --cubefit --sources B C --lines NH3_11 NH3_22
#
import first_look
import numpy as np
from spectral_cube import SpectralCube
import astropy.units as u
from basemask import basebox, chanmin, chanmax
from cloud_keys import keys, WindowDict

def main():
	# Setting up the command line interaction
	import argparse
	parser = argparse.ArgumentParser(description =
	                    'Runs the various data analysis tasks on GBT-15B-313.')
	parser.add_argument('--firstlook', dest='firstlook', 
			    action='store_true', default=False, 
			    help='do simple cube analysis')
	parser.add_argument('--cubefit', dest='cubefit', 
			   action='store_true', default=False, 
			   help='fit spectral cube(s)')
	parser.add_argument('--sources', action='store', nargs='+',
	                   help='source(s) for the pipeline to process')
	parser.add_argument('--lines', action='store', nargs='+',
	                   help='line(s) for the pipeline to process')
	
	args = parser.parse_args()
	# so this is a bit ugly, but it still allows to
	# exectute the main() block through execfile(reduce.py)
	warn = False
	if args.sources is None:
		warn = True
		print parser.format_usage()
		print 'assuming source I'
		print 'consider passing --sources X Y Z',
		print 'from the command line'
		args.sources = ['I']
	if args.lines is None:
		if not warn:
			print parser.format_usage()
		print 'will process all the lines!'
		print 'consider passing --lines X Y Z',
		print 'from the command line'
		# pulls all unique values from {'ifnum':'lineName', ...}:
		lines=[]
		_ = [(WindowDict[ifn],lines.append(WindowDict[ifn])) 
		    	for ifn in WindowDict if WindowDict[ifn] not in lines]
		args.lines = lines

	if args.firstlook:
		for cloud in args.sources:
			for line in args.lines:
				firstlook(cloud=cloud, line=line)
	elif args.cubefit:
		for cloud in args.sources:
			for line in args.lines:
				fitcube(cloud)
	else:
		raise Warning("At least one of --firstlook and --cubefit arguments is required.")

def firstlook(cloud, line='NH3_11'):
	print('Now %s' % line)
	a_rms, b_rms = basebox(cloud, line)
	cmin, cmax = chanmin(cloud, line), chanmax(cloud, line)
	# assuming the peak of emission is somewhere 
	# in the middle of the bandwidth:
	cmid = (cmin+cmax)/2
	# we can find the corresponding gap in basebox:
	bcen, acen = [[i,i+1] for i in range(len(a_rms)-1) 
			if b_rms[i]<cmid<a_rms[i+1]][0]
	index_peak=first_look.create_index([b_rms[bcen]],[a_rms[acen]])
	index_rms=first_look.create_index(a_rms, b_rms)
	
	file_in = '../%s/%s_%s.fits' % (keys[cloud]['region'], 
					keys[cloud]['region'], line)
	s = SpectralCube.read(file_in)
	s = s.with_spectral_unit(u.km/u.s,velocity_convention='radio')
	
	file_out=file_in.replace('.fits','_base1.fits')
	file_new=first_look.baseline(file_in, file_out, 
	                             index_clean=index_rms, polyorder=1)
	first_look.peak_rms(file_new, index_rms=index_rms, 
			    index_peak=index_peak)

def fitcube(cloud='I', lines=['NH3_11', 'NH3_22', 'NH3_33'], blorder=1, do_plot=True, 
	    			snr_min=3, multicore=1, vmax=38, vmin=44):
	for line in lines:
		if not 'NH3_' in line:
			raise Warning("Lines other than ammonia aren't implemented yet.")
	import PropertyMaps # throws an error; TODO: try it with your pyspectkit version
	PropertyMaps.cubefit('cloud'+cloud,blorder,vmin,vmax,do_plot,snr_min,multicore)
	
	raise Warning("Under construction.")

if __name__ == "__main__":
	main()
