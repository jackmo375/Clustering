#!/bin/bash

#
#	COMPARE:
#	compare jump and gap tests for non-globular data 
#
########################################################

# load project file parameters:
. ./config.sh

# check the correct python enviroment is loaded:
check_py_enviroment		# function in config.sh

python ${source}compare.py
