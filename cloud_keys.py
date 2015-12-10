# Stored here: 
# - default parameters for the pipeline
# - variables specific to individual clouds

gains_unity = '1,1,1,1,1,1,1,1,1,1,1,1,1,1'
gains_GAS   = '0.883,0.858,0.885,0.847,0.847,0.855,0.746,0.731,0.986,0.768,0.647,0.522,0.894,1.109'

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
