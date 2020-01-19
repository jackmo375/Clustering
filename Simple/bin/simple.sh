#!/bin/bash

wk='/home/jack/Local/Learning/DataAnalysis/Clustering/Simple/'
source=${wk}'src/'
data=${wk}'data/'
media=${wk}'media/'

python ${source}simple.py

label='simple'
graphFile=${data}${label}'.gv'
if [[ -f ${graphFile} ]]; then
	circo -Tpng ${data}${label}.gv -o ${media}${label}.png
fi

label='points'
graphFile=${data}${label}'.gv'
if [[ -f ${graphFile} ]]; then
	circo -Tpng ${data}${label}.gv -o ${media}${label}.png
fi

label='clusters'
graphFile=${data}${label}'.gv'
if [[ -f ${graphFile} ]]; then
	circo -Tpng ${data}${label}.gv -o ${media}${label}.png
fi
