# preliminary inputs for baseline fitting
import numpy as np

# TODO: merge with keys dictionary in cloud_keys.py
# TODO: create bright spectra for ammonia / gaussians for others,
#	and then create baseline masks by T<Tmax*1e-4 criteria!
#	(that's much easier to understand)

base_11 = {'J':[[65 , 484, 761, 1251, 1605],
      		[289, 614, 832, 1363, 1741] ],
	   'I':[[],[]],
	   'E':[[99 , 449, 1222, 1553],
		[286, 618, 1384, 1747] ],
	   'B':[[],[]],
	   'A':[[],[]] }
baseall = {'A':[],'B':[],'E':[],'I':[],
	   'J':[[141, 1173], 
		[644, 1658] ]}

# TODO: verify! this is just a first baseline estimate!
#	esp. for cloud I, which has a widely separated
#	and unexpectedly strong velocity component
# filling in some default guesses for other clouds/lines
for cloud in ['A','B','E','I']:
	baseall[cloud]=baseall['J']
for cloud in ['A','B','I']:
	base_11[cloud]=base_11['E']

def basebox(cloud, line):
	return np.asarray(base_11[cloud]) if line is 'NH3_11' else np.asarray(baseall[cloud])

def chanmin(cloud, line):
	return min(basebox(cloud, line)[0])

def chanmax(cloud, line):
	return max(basebox(cloud, line)[1])
