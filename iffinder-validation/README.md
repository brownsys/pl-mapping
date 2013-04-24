generateFixedData.py
=============================

Description
------------
Checks for IPs which have identical DNS records in weeks surrounding a given week, but do not appear in that week. These IPs should not be omitted from that week and are probably only omitted due to scripting mistakes. This script generates new versions of COGENT-MASTER-ATLAS.txt files containing these fixed entries.

Usage
------
./generateFixedData.py dnsRecords [outputDirectory]
dnsRecords - directory containing weeks of DNS records in subdirectories, probably "pl_archives/"
outputDirectory - Optionally output fixed files to a new directory, otherwise files are placed in the directory specified by dnsRecords


Example
--------

### Generate fixed files into a directory called "fixed"
./generateFixedData.py pl_archives fixed


getMissingIPs.py
=============================

Description
------------
This script looks for anomalies in the iffinder/DNS data from week to week. It specifically looks for IPs which appear in week N-1, not in week N, and then again in week N+1. It prints anomalies to stdout and stats about the anomalies to stderr. Anomalies are classified into three cases:
# 1. IP has same DNS record in prev and next
# OR IP has different DNS record and:
#	2. DNS record from prev belongs to other IPs
#	3. DNS record from prev has disappeared 

Usage
------
./getMissingIPs.py dnsRecords [weekNumbers] [options]
dnsRecords - directory containing weeks of DNS records in subdirectories, probably "pl_archives/"
weekNumbers - whitespace separated week numbers of interest. there can be as many as desired. when omitted all weeks are analyzed.

Options
--------
--onlyDisappeared - only print IPs in case 1
--detailed - output give more information about how the DNS record change over the three week period analyzed
--raw - prints output with less text that's easier to look at
