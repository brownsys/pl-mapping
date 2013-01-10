#!/bin/bash

archive_dir=/home/adf/pl_archives
iffinder_dst=/home/adf/pl_iffinder-results
iffinder_src=/home/adf/results

last_archive=`ls -1 $archive_dir | sort -n | tail -1`

scp -p -q "quanto:$iffinder_src/$last_archive-*" $iffinder_dst
