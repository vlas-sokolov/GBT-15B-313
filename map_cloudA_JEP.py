
import GAS_gridregion
import textwrap
import sys
import os

from astropy.io import fits

# TODO: will be repeated, but everything except for LPCs should be ok

# Daisy scan numbers:
# 16:18,23:34 | mapped those with a wrong value of vlsr in source.cat (30 instead of 65.8 km/s)
# 70:81,84:86 | daisy scans at the end of the run, with corrected vlsr value

# don't use AIPS at all... it is really ugly!
gbt_dir='/lustre/pipeline/scratch/vsokolov'

# run the pipeline
gbtpipeline --clobber -u tmb --window 2 -m "70:81,84:86" -f 0,1,3,4,5,6 -i /home/scratch/vsokolov/AGBT15B_313_03.raw.vegas
