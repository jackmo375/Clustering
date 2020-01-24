#!/bin/bash

. ./config.sh

label=$1

python ${source}simple.py $label

convert -border 160x160 -bordercolor "#FFFFFF" ${media}${label}'2.png' ${media}${label}'2.png'

convert ${media}${label}'1.png' ${media}${label}'2.png' +append ${media}${label}'.png'

rm ${media}${label}'1.png' ${media}${label}'2.png'