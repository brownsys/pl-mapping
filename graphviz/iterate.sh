#!/bin/bash

DATA=/research/cogent_map/pl_archives
BIN=$HOME/work/projects/pl-mapping/graphviz

for i in $( ls -1 $DATA); do
	cat $DATA/$i/cogent_pairs_matching_hw.txt | $BIN/make-gv.py > cogent_pairs_matching_hw_routers_real.$i.dot
	cat $DATA/$i/cogent_pairs_matching_hw.txt | $BIN/make-gv-cities.py > cogent_pairs_matching_hw_cities.$i.dot
done

