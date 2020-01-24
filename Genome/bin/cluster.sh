#!/bin/bash

#
#	CLUSTER:
#	plot genome clusters
#
########################################################

# load project file parameters:
. ./config.sh

# check the correct python enviroment is loaded:
check_py_enviroment		# function in config.sh

label=$1

python ${source}cluster.py $label

# resize graph plot and add white border
convert -border 60x60 -bordercolor "#FFFFFF" ${media}${label}'2.png' ${media}${label}'2.png'
convert ${media}${label}'2.png' -resize 1000x1000\> ${media}${label}'2.png'

# combine plots into single image
convert \
	${media}${label}'1.png' \
	${media}${label}'2.png' \
	+append ${media}${label}'.png' 

# remove temporary plot files:
rm ${media}${label}'1.png' ${media}${label}'2.png'