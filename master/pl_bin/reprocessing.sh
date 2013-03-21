#!/bin/bash

bin_dir=/home/adf/RouterPeek/pl-mapping/master/pl_bin/

# split into different parts of Cogent IP space

for i in `ls -1 rev-*-1?.txt.gz rev-*-2?.txt.gz`; do
	base=`echo $i | awk -F".t" '{ print $1 }'` 
	cogentco="$base-cogent.txt"
	atlas="$base-cogent-atlas.txt"
	demarc="$base-cogent-demarc.txt"
	other="$base-cogent-other.txt"
    cat $cogentco | egrep "(atlas\.cogentco\.com|altas\.cogentco\.com|atlasc\.cogentco\.com)" > $atlas
	cat $cogentco | egrep '(demarc\.cogentco\.com|dmarc\.cognetco\.com|demar\.cogentco\.com|dmark\.cogentco\.com|demark\.cogentco\.com|demarco\.cogentco\.com|demarch\.cogentco\.com|DEMArc\.cogentco\.com|demarac\.cogentco\.com|demearc\.cogentco\.com|demac\.cogentco\.com|demrac\.cogentco\.com|DEMARC\.cogentco\.com|denarc\.cogentco\.com)' > $demarc
	cat $cogentco | grep -v "atlas.cogentco.com" | grep -v "altas.cogentco.com" | grep -v "atlasc.cogentco.com" | grep -v "demarc.cogentco.com" | grep -v "dmarc.cogentco.com" | grep -v "demar.cogentco.com" | grep -v "dmark.cogentco.com" | grep -v "demark.cogentco.com" | grep -v "demarco.cogentco.com" | grep -v "demarch.cogentco.com" | grep -v "DEMArc.cogentco.com" | grep -v "demarac.cogentco.com" | grep -v "demearc.cogentco.com" | grep -v "demac.cogentco.com" | grep -v "demrac.cogentco.com" | grep -v "DEMARC.cogentco.com" | grep -v "denarc.cogentco.com" > $other
done

# categorize the *.(atlas|altas|atlasc).cogentco.com addresses
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

num_nxdomain=`cat SUMMARY.txt | grep NXDOMAIN | awk -F": " '{ print $2 }'`
num_servfail=`cat SUMMARY.txt | grep SERVFAIL | awk -F": " '{ print $2 }'`
num_refused=`cat SUMMARY.txt | grep REFUSED | awk -F": " '{ print $2 }'`
num_timeout=`cat SUMMARY.txt | grep timeout | awk -F": " '{ print $2 }'`

num_alias=`wc -l rev-all_alias.txt`
num_no_ptr=`wc -l rev-all_no_ptr.txt`
num_anomoly_lines=`wc -l rev-all_anomoly.txt`

##
## Empty SUMMARY.txt
rm SUMMARY.txt
##

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
