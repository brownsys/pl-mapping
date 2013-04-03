#!/bin/bash

start_week=2
last_week=53

output_dir=/research/cogent_map/iffinder-analysis
dns_in_dir=/research/cogent_map/pl_archives
iffinder_in_dir=/research/cogent_map/pl_iffinder-results

parse_script=/home/adf/RouterPeek/pl-mapping/iffinder-validation/parseData.py

pushd $output_dir

i=$start_week

while [ $i -lt $((last_week + 1)) ]; do
	echo "Processing week: $i ..."

	$parse_script $iffinder_in_dir/$i-*-iffinder.txt $dns_in_dir/$i/COGENT-MASTER-ATLAS.txt 2>$i.stderr.txt 1>$i.stdout.txt

	i=$((i+1))
done

popd
