#!/bin/bash

# Add to sputnik's crontab:
# 0 20 * * Wed /home/adf/RouterPeek/pl-mapping/support/pl-copy-to-dept.sh

archive_src="rest:/home/adf/pl_archives"
archive_dst=/research/cogent_map/pl_archives

iffinder_src="rest:/home/adf/pl_iffinder-results"
iffinder_dst=/research/cogent_map/pl_iffinder-results

cd $archive_dst

last_archive=`/bin/ls -1 | sort -n | tail -1`
next_archive=$((last_archive + 1))

scp -p -q -r "$archive_src/$next_archive" .

cd $iffinder_dst

scp -p -q "$iffinder_src/$next_archive-*" .
