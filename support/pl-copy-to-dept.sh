#!/bin/bash

# Add to sputnik's crontab:
# 0 20 * * Wed /home/adf/RouterPeek/pl-mapping/support/pl-copy-to-dept.sh

scp_cmd="scp -p -q"

archive_src="rest:/home/adf/pl_archives"
archive_dst=/research/cogent_map/pl_archives

iffinder_src="rest:/home/adf/pl_iffinder-results"
iffinder_dst=/research/cogent_map/pl_iffinder-results

cd $archive_dst

last_archive=`/bin/ls -1 | sort -n | tail -1`
next_archive=$((last_archive + 1))

$scp_cmd -r "$archive_src/$next_archive" .

cd $iffinder_dst

$scp_cmd "$iffinder_src/$next_archive-*" .

###
#
# Add each week to the released data sets
#
###

i=$next_archive

cd /research/cogent_map/data_release/

cp -a $archive_dst/$i .
cp -a $iffinder_dst/$i-*-iffinder.txt iffinder/

times=`(cat $i/pl_mapping.sql | grep -v LOCK | sed "s/) ENGINE.*/);/" | sed "s/),(/);\nINSERT INTO pl_mapping VALUES(/g"; echo "SELECT MIN(work_started), MAX(last_contact) FROM pl_mapping;") | sqlite3 | tr "|" ","`
echo "$i,$times" >> interval-timestamps.csv.txt

zpaq a $i-raw.zpaq $i/rev-* -quiet 2>&1 | grep -v "No such file"
rm $i/rev-*
zpaq a $i-processed.zpaq $i/ -quiet 2>&1 | grep -v "No such file"
rm -rf $i

mv $i-processed.zpaq processed/$i.zpaq
mv $i-raw.zpaq raw/$i.zpaq

gzip iffinder/$i-*-iffinder.txt

openssl sha1 processed/$i.zpaq >> processed.sha1.txt
openssl sha1 raw/$i.zpaq >> raw.sha1.txt
openssl sha1 iffinder/$i-*-iffinder.txt.gz >> iffinder.sha1.txt

$scp_cmd processed/$i.zpaq systems:/vol/web/html/cogent/processed/
$scp_cmd raw/$i.zpaq systems:/vol/web/html/cogent/raw/
$scp_cmd iffinder/$i-*-iffinder.txt.gz systems:/vol/web/html/cogent/iffinder/
$scp_cmd processed.sha1.txt systems:/vol/web/html/cogent/
$scp_cmd raw.sha1.txt systems:/vol/web/html/cogent/
$scp_cmd iffinder.sha1.txt systems:/vol/web/html/cogent/
$scp_cmd interval-timestamps.csv.txt systems:/vol/web/html/cogent/
