#!/bin/bash

pl_web_dir=/var/www/pl-mapping
output_dir=$pl_web_dir/pl-uploads
archive_dir=/home/adf/pl_archives
bin_dir=/home/adf/pl_bin
marker_file=$output_dir/__MAPPING_COMPLETE__

##
# Sanity checks
##

if [ "`whoami`" != "root" ]; then
	echo "$0 must be run as root"
	exit
fi

last_archive=`ls -1 $archive_dir | sort -n | tail -1`
new_archive=$(($last_archive + 1))

if [ -d "$archive_dir/$new_archive" ]; then
	echo "FAIL. $archive_dir/$new_archive exists!!"
	echo "Cowardly refusing to overwrite new directory."
	exit
fi

if [ -f "$marker_file" ]; then
    rm "$marker_file"
else
    exit
fi

##
# Process completed mapping results!
##

# dump table to preserve timestamps
mysqldump -u pl_mapping -ppl_mapping pl_mapping > $output_dir/pl_mapping.sql

# move all files (incl. error log) to archive location
mkdir $archive_dir/$new_archive/
mv $output_dir/* $archive_dir/$new_archive/

# generate new IP listings
pushd $pl_web_dir
php pl-generate-ips.php
popd

# apply the processing scripts

pushd $archive_dir/$new_archive/

# split into different parts of Cogent IP space
$bin_dir/pl-partition.sh
cat rev-*.*.*.*-??.txt | grep "is an alias for" > rev-all_alias.txt
cat rev-*.*.*.*-??.txt | grep "has no PTR" > rev-all_no_ptr.txt
cat rev-*.*.*.*-??.txt | grep -v NXDOMAIN | grep -v SERVFAIL | grep -v REFUSED | grep -v "connection timed out" | grep -v "is an alias for" | grep -v "domain name pointer" | grep -v "retrying in TCP" | grep -v "has no PTR" > rev-all_anomoly.txt

# categorize the *.atlas.cogentco.com addresses
cat *-atlas.txt | $bin_dir/sort-atlas.py | sort > COGENT-MASTER-ATLAS.txt

# find the /30 address pairs
cat COGENT-MASTER-ATLAS.txt | $bin_dir/collect-pairs.py > cogent_pairs.txt
cat cogent_pairs.txt | awk '{ if ($2 == $6) print $0 }' > cogent_pairs_matching_hw.txt
cat cogent_pairs.txt | awk '{ if ($2 != $6) print $0 }' > cogent_pairs_non-matching_hw.txt
cat cogent_pairs_non-matching_hw.txt | grep Vlan > cogent_pairs_non-matching_hw-vlan.txt
cat cogent_pairs_non-matching_hw.txt | grep oob > cogent_pairs_non-matching_hw-oob.txt
cat cogent_pairs_non-matching_hw.txt | grep "(unknown)" > cogent_pairs_non-matching_hw-unknown.txt
cat cogent_pairs_non-matching_hw.txt | grep IntegratedServicesModule > cogent_pairs_non-matching_hw-IntegratedServicesModule.txt
cat cogent_pairs_non-matching_hw.txt | grep -v Vlan | grep -v oob | grep -v "(unknown)" | grep -v IntegratedServicesModule > cogent_pairs_non-matching_hw-others.txt

num_exist=`wc *-exists.txt | tail -1 | awk '{ print $1 }'`
num_atlas=`wc *-cogent-atlas.txt | tail -1 | awk '{ print $1 }'`
num_demarc=`wc *-cogent-demarc.txt | tail -1 | awk '{ print $1 }'`
num_cogent_other=`wc *-cogent-other.txt | tail -1 | awk '{ print $1 }'`
num_non_cogent=$(( $num_exist - $num_atlas - $num_demarc - $num_cogent_other ))
num_nxdomain=`cat rev-*.*.*.*-??.txt | grep NXDOMAIN | wc -l`
num_servfail=`cat rev-*.*.*.*-??.txt | grep SERVFAIL | wc -l`
num_refused=`cat rev-*.*.*.*-??.txt | grep REFUSED | wc -l`
num_timeout=`cat rev-*.*.*.*-??.txt | grep "connection timed out" | wc -l`
num_alias=`wc -l rev-all_alias.txt`
num_no_ptr=`wc -l rev-all_no_ptr.txt`
num_anomoly_lines=`wc -l rev-all_anomoly.txt`

echo "Num exist: $num_exist" >> SUMMARY.txt
echo "Num atlas: $num_atlas" >> SUMMARY.txt
echo "Num demarc: $num_demarc" >> SUMMARY.txt
echo "Num cogent other: $num_cogent_other" >> SUMMARY.txt
echo "Num non-cogent: $num_non_cogent" >> SUMMARY.txt
echo "Num NXDOMAIN: $num_nxdomain" >> SUMMARY.txt
echo "Num SERVFAIL: $num_servfail" >> SUMMARY.txt
echo "Num REFUSED: $num_refused" >> SUMMARY.txt
echo "Num timeout: $num_timeout" >> SUMMARY.txt
echo "Num alias: $num_alias" >> SUMMARY.txt
echo "Num no PTR: $num_no_ptr" >> SUMMARY.txt
echo "Num anomoly lines: $num_anomoly_lines" >> SUMMARY.txt

# ? maybe more like http://trace.cs.brown.edu/wiki/Internal/Cogent_Atlas
# ... note, those tables get mixed-up by "JFK" vs "jfk"

# TODO: we'll also want to extract candidate alias sets to compare with, and then do immediate lookups to confirm
# (that is for post-processing the iffinder results)
cat COGENT-MASTER-ATLAS.txt | awk '{ print $(NF - 1) }' > cogent-all-ips.txt
shuf cogent-all-ips.txt > cogent-all-ips.random-order.txt
rm cogent-all-ips.txt
sudo -u adf scp cogent-all-ips.random-order.txt quanto.cs.brown.edu:/home/adf/$new_archive-cogent-all-ips.random-order.txt
rm cogent-all-ips.random-order.txt
# TODO: then, on quanto, something like:
# sudo ./iffinder -c3 -r1 <ip_file> > <out file>    <-- -r1 is 1 per second, so the Cogent atlas should take less than 12 hours

# finally, compress raw input files

for i in `ls -1 rev-*.*.*.*-??.txt`; do
	gzip $i
done

popd

chown -R adf.adf $archive_dir/$new_archive/
