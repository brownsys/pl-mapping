#!/bin/bash

# Reprocessing script based on April 2, 2013 changes

#
# Now, reconsolidate
#

ls -1 rev-*-exists.txt | sort -V | xargs cat > all_exists.txt

rm rev-*-exists.txt

ls -1 rev-*-cogent-atlas.txt | sort -V | xargs cat > cogent-atlas.txt
ls -1 rev-*-cogent-demarc.txt | sort -V | xargs cat > cogent-demarc.txt
ls -1 rev-*-cogent-other.txt | sort -V | xargs cat > cogent-other.txt

rm rev-*-cogent-atlas.txt
rm rev-*-cogent-demarc.txt
rm rev-*-cogent-other.txt

#
# And cleanup
#

rm rev-*-cogent.txt

###
### Reprocessing
###

touch cogent-dial.txt
mv rev-all_alias.txt all_alias.txt
mv rev-all_no_ptr.txt all_no_ptr.txt
mv rev-all_anomoly.txt all_anomaly.txt

##

num_exist=`wc all_exists.txt | awk '{ print $1 }'`
num_atlas=`wc cogent-atlas.txt | awk '{ print $1 }'`
num_demarc=`wc cogent-demarc.txt | awk '{ print $1 }'`
num_dial=`wc cogent-dial.txt | awk '{ print $1 }'`
num_cogent_other=`wc cogent-other.txt | awk '{ print $1 }'`
num_non_cogent=$(( $num_exist - $num_atlas - $num_demarc - $num_dial - $num_cogent_other ))

num_nxdomain=`cat SUMMARY.txt | grep NXDOMAIN | awk -F": " '{ print $2 }'`
num_servfail=`cat SUMMARY.txt | grep SERVFAIL | awk -F": " '{ print $2 }'`
num_refused=`cat SUMMARY.txt | grep REFUSED | awk -F": " '{ print $2 }'`
num_timeout=`cat SUMMARY.txt | grep timeout | awk -F": " '{ print $2 }'`

num_alias=`wc -l all_alias.txt`
num_no_ptr=`wc -l all_no_ptr.txt`
num_anomaly_lines=`wc -l all_anomaly.txt`

##
## Empty SUMMARY.txt
rm SUMMARY.txt
##

echo "Num exist: $num_exist" >> SUMMARY.txt
echo "Num atlas: $num_atlas" >> SUMMARY.txt
echo "Num demarc: $num_demarc" >> SUMMARY.txt
echo "Num dial: $num_dial" >> SUMMARY.txt
echo "Num cogent other: $num_cogent_other" >> SUMMARY.txt
echo "Num non-cogent: $num_non_cogent" >> SUMMARY.txt
echo "Num NXDOMAIN: $num_nxdomain" >> SUMMARY.txt
echo "Num SERVFAIL: $num_servfail" >> SUMMARY.txt
echo "Num REFUSED: $num_refused" >> SUMMARY.txt
echo "Num timeout: $num_timeout" >> SUMMARY.txt
echo "Num alias: $num_alias" >> SUMMARY.txt
echo "Num no PTR: $num_no_ptr" >> SUMMARY.txt
echo "Num anomaly lines: $num_anomaly_lines" >> SUMMARY.txt

# and also compress some of the bigger outputs

gzip all_exists.txt
gzip cogent-atlas.txt
gzip cogent-dial.txt
