#!/bin/bash

#	ELBOW:
#	perform elbow test for cluster analysis
#
###########################################

# load project file parameters:
. ./config.sh

# check project enviroment is loaded:
env=$(which python)
if [[ $env != *${pyenv}* ]]; then
	echo 'current python enviroment is: '$env
	echo 'ERROR: please load the correct python enviroment and try again.'
	exit 1
fi

# run python script:
python ${source}elbow.py
