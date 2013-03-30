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
    cat $cogentco | egrep "(atlas\.cogentco\.com|altas\.cogentco\.com|atlasc\.cogentco\.com)" > $atlas
	cat $cogentco | egrep '(demarc\.cogentco\.com|dmarc\.cognetco\.com|demar\.cogentco\.com|dmark\.cogentco\.com|demark\.cogentco\.com|demarco\.cogentco\.com|demarch\.cogentco\.com|DEMArc\.cogentco\.com|demarac\.cogentco\.com|demearc\.cogentco\.com|demac\.cogentco\.com|demrac\.cogentco\.com|DEMARC\.cogentco\.com|denarc\.cogentco\.com)' > $demarc
	cat $cogentco | grep -v "atlas.cogentco.com" | grep -v "altas.cogentco.com" | grep -v "atlasc.cogentco.com" | grep -v "demarc.cogentco.com" | grep -v "dmarc.cogentco.com" | grep -v "demar.cogentco.com" | grep -v "dmark.cogentco.com" | grep -v "demark.cogentco.com" | grep -v "demarco.cogentco.com" | grep -v "demarch.cogentco.com" | grep -v "DEMArc.cogentco.com" | grep -v "demarac.cogentco.com" | grep -v "demearc.cogentco.com" | grep -v "demac.cogentco.com" | grep -v "demrac.cogentco.com" | grep -v "DEMARC.cogentco.com" | grep -v "denarc.cogentco.com" > $other
#	echo "$base finished"
done
