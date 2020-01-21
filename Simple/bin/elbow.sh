#!/bin/bash

#	ELBOW:
#	perform elbow test for cluster analysis
#
###########################################

# load project file parameters:
. ./config.sh

# check project enviroment is loaded:
check_py_enviroment		# call of function from config.sh

# run python script:
python ${source}elbow.py
