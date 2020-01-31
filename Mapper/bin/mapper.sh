#!/bin/bash

#
#	MAPPER:
#	our implementation of the mapper algorithm
#
########################################################

# load project file parameters:
. ./config.sh

# check the correct python enviroment is loaded:
check_py_enviroment		# function in config.sh

python ${source}mapper.py
