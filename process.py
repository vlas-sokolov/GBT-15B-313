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

def fitcube(cloud='I', lines=['NH3_11', 'NH3_22', 'NH3_33','NH3_44','NH3_55'], blorder=1, do_plot=True, snr_min=6.5, multicore=1, vmin=38, vmax=44):
	import pyspeckit
	for line in lines:
		if not 'NH3_' in line:
			raise Warning("Lines other than ammonia aren't implemented yet.")
	try:
		# TODO: implement "lines" argument
		import i_want_this_to_fail_for_now
		import PropertyMaps # throws an error; TODO: try it with your pyspectkit version
		PropertyMaps.cubefit('cloud'+cloud,blorder,vmin,vmax,do_plot,snr_min,multicore)
	except ImportError: # if we're out of GAS
		fitsdir = 'cloud'+cloud+'/'
		nh3files = []
		for line in lines:
			nh3files.append(fitsdir+'cloud%s_%s_base%s.fits' % 
							(cloud, line, blorder))
		
		# taken from PropertyMaps.py
		from spectral_cube import SpectralCube
		from astropy.io import fits
		errmap11 = fits.getdata('cloudI/cloudI_NH3_11_base1_rms.fits')
		cube11sc = SpectralCube.read(nh3files[0])
		snr = cube11sc.filled_data[:].value/errmap11
		peaksnr = np.max(snr,axis=0)
		rms = np.nanmedian(errmap11)
		planemask = (peaksnr>snr_min)
		try:
			guesses=fits.getdata('Ipars.fits')[:6,:,:]
		except:
			print "Can't read par.maps fits file!"
			guesses=[15,3,15,0.2,40,0.5]
		cubelst = []
		for f in nh3files: cubelst.append(pyspeckit.Cube(f,maskmap=planemask))
		cubes=pyspeckit.CubeStack(cubelst)
		T,F = True,False
		cubes.fiteach(fittype='ammonia',
			      guesses=guesses,
			      integral=False,
			      verbose_level=3,
			      fixed=[F,F,F,F,F,T],
			      signal_cut=snr_min,
			      limitedmax=[T,T,T,T,T,T],
			      limitedmin=[T,T,T,T,T,T],
			      maxpars=[30,7,20,5,vmax,1],
			      minpars=[0,0,0,0,vmin,0],
			      start_from_point=(21,21), # redudndant with position_order
			      use_neighbor_as_guess=True,
			      position_order= 1/peaksnr,
			      errmap=errmap11,
			      multicore=multicore)

		# taken from PropertyMaps.py
		fitcubefile = fits.PrimaryHDU(data=np.concatenate([cubes.parcube,cubes.errcube]), header=cubes.header)
                for h1,h2 in zip(['1','2','3','4','5','6','7','8','9','10','11','12'],
                                 ['TKIN','TEX','COLUMN','SIGMA','VELOCITY','FORTHO',
                                  'eTKIN','eTEX','eCOLUMN','eSIGMA','eVELOCITY','eFORTHO']):
                        fitcubefile.header.update(h1,h2)
		fitcubefile.header.update('CDELT3',1)
		fitcubefile.header.update('CTYPE3','FITPAR')
		fitcubefile.header.update('CRVAL3',0)
		fitcubefile.header.update('CRPIX3',1)
		fitcubefile.writeto("cloud{0}_parameter_maps.fits".format(cloud),clobber=True)

		if do_plot:
			cubes.mapplot()
			#cubes.mapplot.plane = cubes.parcube[0,:,:]
			#cubes.mapplot(estimator=None)

if __name__ == "__main__":
	main()
