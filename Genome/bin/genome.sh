#!/bin/bash

#
#	JUMP:
#	perform jump test
#	(gap test adapted for hierarchical cluster analysis) 
#
########################################################

# load project file parameters:
. ./config.sh

# check the correct python enviroment is loaded:
check_py_enviroment		# function in config.sh

python ${source}genome.py
