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

###
#
# Add each week to the released data sets
#
###

i=$next_archive

cd /research/cogent_map/data_release/

cp -a $archive_dst/$i .

zpaq a $i-raw.zpaq $i/rev-*
rm $i/rev-*
zpaq a $i-processed.zpaq $i/
rm -rf $i

mv $i-processed.zpaq processed/$i.zpaq
mv $i-raw.zpaq raw/$i.zpaq

openssl sha1 processed/$i.zpaq >> processed.sha1.txt
openssl sha1 raw/$i.zpaq >> raw.sha1.txt

scp processed/$i.zpaq systems:/vol/web/html/cogent/processed/
scp raw/$i.zpaq systems:/vol/web/html/cogent/raw/
scp processed.sha1.txt systems:/vol/web/html/cogent/
scp raw.sha1.txt systems:/vol/web/html/cogent/
