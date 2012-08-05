#!/bin/bash

trap "" 1 # Eat the NOHUP signal

input=$1

cd /home/adf/

if [ ! -f "$input" ]; then
	echo "Input file not found!"
	exit
fi

base=`echo $input | awk -F".txt" '{ print $1 }'`
output="$base-iffinder.txt"

sudo /home/adf/iffinder-1.37/iffinder -v0 -c3 -r1 $input > $output 2>&1

mv $input results/
mv $output results/
