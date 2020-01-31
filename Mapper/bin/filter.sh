#!/bin/bash

#
#	FILTER:
#	**another** precursor to the mapper algorithm: test
#	simple filter functions directly on the data, like
#	L-infinity centrality or kernal density estimates,
#	before we get to the mapper algorithm.
#
########################################################

# load project file parameters:
. ./config.sh

# check the correct python enviroment is loaded:
check_py_enviroment		# function in config.sh

python ${source}filter.py
