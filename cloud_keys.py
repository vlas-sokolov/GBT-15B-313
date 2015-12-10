# Stored here: 
# - default parameters for the pipeline
# - variables specific to individual clouds

gains_unity = '1,1,1,1,1,1,1,1,1,1,1,1,1,1'
gains_GAS   = '0.883,0.858,0.885,0.847,0.847,0.855,0.746,0.731,0.986,0.768,0.647,0.522,0.894,1.109'

# TODO: convert into a text table format to be read with scipy or pandas

keys = {'A':{}, 'B':{}, 'C':{}, 'I':{}, 'J':{}}

keys['A'] = {
	'session': 03,
	'source' : 'AG18.82',
	'region' : 'cloudA',
	'windows': ['0','1','2','3','4','5','6'],
	'nblocks': 2,
	'scans'  : [{'start':70, 'end':81},
		    {'start':84, 'end':86} ],
	'gains'  : gains_unity
	}

keys['B'] = {
	'session': 03,
	'source' : 'BG19.27',
	'region' : 'cloudB',
	'windows': ['0','1','2','3','4','5','6'],
	'nblocks': 1,
	'scans'  : [{'start':49, 'end':60}],
	'gains'  : gains_unity
	}

keys['E'] = {
	'session': 03,
	'source' : 'EG28.67',
	'region' : 'cloudE',
	'windows': ['0','1','2','3','4','5','6'],
	'nblocks': 1,
	'scans'  : [{'start':87, 'end':98}],
	'gains'  : gains_unity
	}

keys['I'] = {
	'session': 03,
	'source' : 'IG38.35',
	'region' : 'cloudI',
	'windows': ['0','1','2','3','4','5','6'],
	'nblocks': 2,
	'scans'  : [{'start':20, 'end':31},
		    {'start':45, 'end':48} ],
	'gains'  : gains_unity
	}

keys['J'] = {
	'session': 03,
	'source' : 'JG53.11',
	'region' : 'cloudJ',
	'windows': ['0','1','2','3','4','5','6'],
	'nblocks': 1,
	'scans'  : [{'start':105, 'end':112}],
	'gains'  : gains_unity
	}
