#!/bin/sh

for i in `ls -1 rev-*-1?.txt rev-*-2?.txt`; do
	base=`echo $i | awk -F".t" '{ print $1 }'`
	exists="$base-exists.txt"
	cogentco="$base-cogent.txt"
	atlas="$base-cogent-atlas.txt"
	demarc="$base-cogent-demarc.txt"
	other="$base-cogent-other.txt"
#	echo "$base starting"
#	cat $i | grep -v NXDOMAIN | grep -v SERVFAIL | grep -v "connection timed out" > $exists
	cat $i | grep "domain name pointer" > $exists
	cat $exists | grep "cogentco.com" > $cogentco
	cat $cogentco | grep "atlas.cogentco.com" > $atlas
	cat $cogentco | egrep '(demarc\.cogentco\.com|dmarc\.cognetco\.com|demar\.cogentco\.com|dmark\.cogentco\.com|demark\.cogentco\.com)' > $demarc
	cat $cogentco | grep -v "atlas.cogentco.com" | grep -v "demarc.cogentco.com" | grep -v "dmarc.cogentco.com" | grep -v "demar.cogentco.com" | grep -v "dmark.cogentco.com" | grep -v "demark.cogentco.com" > $other
#	echo "$base finished"
done
