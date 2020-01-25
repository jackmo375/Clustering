#!/bin/bash

#
#	SHAPE:
#	a precursor to the mapper algorithm: output simple
#	size and shape moments, including a histogram, to 
# 	understand the shape of each cluster.  
#
########################################################

# load project file parameters:
. ./config.sh

# check the correct python enviroment is loaded:
check_py_enviroment		# function in config.sh

python ${source}shape.py
