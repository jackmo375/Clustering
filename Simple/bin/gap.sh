#!/bin/bash

#
#	GAP:
#	perform the gap test for cluster analysis
#
###################################################

# load project file parameters:
. ./config.sh

# check the correct python enviroment is loaded:
check_py_enviroment		# function in config.sh

python ${source}gap.py