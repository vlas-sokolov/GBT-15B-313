# Stored here: 
# - default parameters for the pipeline
# - variables specific to individual clouds

# The default gains should be 1's
# the gains derived from GAS on semester 15B are below, and they 
# provide a good intrabeam calibration; however, there could be 
# a small global correction to get the amplitude calibration right.
gains_unity = '1,1,1,1,1,1,1,1,1,1,1,1,1,1'
gains_GAS   = '0.883,0.858,0.885,0.847,0.847,0.855,0.746,0.731,0.986,0.768,0.647,0.522,0.894,1.109'
# selecting all the windows by default
windows     = [str(i) for i in range(14)]

# if set to NaN will be calculated based of RESTFRQ in the header!
beam_NH3_11 = 0.008844151746708757 # in degrees

WindowDict = {'0':'NH3_44',
    	      '1':'NH3_44',
              '2':'NH3_11',
              '3':'NH3_11',
              '4':'NH3_22',
              '5':'NH3_22',
              '6':'NH3_33',
              '7':'NH3_33',
              '8':'HC5N',
              '9':'HC5N',
              '10':'HC7N',
              '11':'HC7N',
              '12':'NH3_55',
              '13':'NH3_55'}

# TODO: convert into a text table format to be read with scipy or pandas

keys = {'A':{}, 'B':{}, 'C':{}, 'I':{}, 'J':{}}

keys['A'] = {
	'source' : 'AG18.82',
        'vlsr'   : 65.8,
	'region' : 'cloudA',
	'windows': windows,
	'nblocks': 2,
	'scans'  : [{'start':70, 'end':81, 'session':03},
		    {'start':84, 'end':86, 'session':03} ],
	'gains'  : gains_unity,
	'beam'   : beam_NH3_11
	}

keys['B'] = {
	'source' : 'BG19.27',
        'vlsr'   : 26.2,
	'region' : 'cloudB',
	'windows': windows,
	'nblocks': 1,
	'scans'  : [{'start':49, 'end':60, 'session':03}],
	'gains'  : gains_unity,
	'beam'   : beam_NH3_11
	}

keys['E'] = {
	'source' : 'EG28.67',
        'vlsr'   : 79.5,
	'region' : 'cloudE',
	'windows': windows,
	'nblocks': 2,
	'scans'  : [{'start':87, 'end':98, 'session':04}, 
		    {'start':28, 'end':35, 'session':05} ],
	'gains'  : gains_unity,
	'beam'   : beam_NH3_11
	}

keys['I'] = {
	'source' : 'IG38.35',
        'vlsr'   : 41.6,
	'region' : 'cloudI',
	'windows': windows,
	'nblocks': 2,
	'scans'  : [{'start':20, 'end':31, 'session':02},
		    {'start':45, 'end':48, 'session':02} ],
	'gains'  : gains_unity,
	'beam'   : beam_NH3_11
	}

keys['J'] = {
	'source' : 'JG53.11',
        'vlsr'   : 22.0,
	'region' : 'cloudJ',
	'windows': windows,
	'nblocks': 2,
	'scans'  : [{'start':105, 'end':112, 'session':04},
		    {'start': 41, 'end': 47, 'session':05} ],
	'gains'  : gains_unity,
	'beam'   : beam_NH3_11
	}
