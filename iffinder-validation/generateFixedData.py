#!/usr/bin/python
"""
This script looks for anomalies in the iffinder/DNS data from week to week.
It specifically looks for IPs which appear in week N-1, not in week N, and
then again in week N+1. It prints anomalies to stdout.

It then rewrites a new set of iffinder/DNS data with wrongly omitted entries
added back in. These
"""
import sys
import re
import operator
import os
import shutil

fixedFilename = "COGENT-MASTER-ATLAS-FIXED.txt"

# determines how strict we should be about the DNS record names.
#
# if set to True, we consider these interfaces to be on the same router:
#     gi1-38.3504.ccr01.jfk03.atlas.cogentco.com
#     gi1-43.3501.ccr01.jfk03.atlas.cogentco.com
# by dropping "3504" and "3501" respectively from each interface name

nonStrictNames = True

"""
Constructs a name from a list of subdomains gathered from DNS queries.
"""
def constructName(nameList):
	if nonStrictNames:
		# remove purely numeric entries from list
		newList = []
		for item in nameList:
			if not item.isdigit():
				newList.append(item)
		nameList = newList
	if len(nameList) >= 4:
		typeOfInterface = nameList[0]
		routerSubIdentifier = nameList[1]
		routerIdentifier = nameList[2]
		location = nameList[3]
		return ".".join([location, routerIdentifier, routerSubIdentifier])
	if len(nameList) == 3:
		typeOfInterface = nameList[0]
		routerIdentifier = nameList[1]
		location = nameList[2]
		return ".".join([location, routerIdentifier])
	else:
		nameList.reverse()
		return ".".join(nameList)


"""
Read reverse DNS records and parse it into tuples structured as follows:

	(domain, IP, type of interface, [subdomains])

Then these tuples are loaded into an IP -> name dictionary and a reverse
dictionary.

Subdomains are ususally of the form:
	
	[interface type code, location, router identifier]
"""
def parseDNSRecords(source, keepRecords):
	# parse the file into usable tuples
	parsed = []
	for line in source.readlines():
		splitLine = re.split("\s+", line.strip())
		parsed.append((splitLine[-3], splitLine[-2], splitLine[-1], splitLine[:-3][::-1]))

	# build dictionaries
	ipToName = {}
	nameToIPs = {}
	duplicateIPs = set()
	ipToRecord = {}
	
	for entry in parsed:
		dnsRecord = entry[0]
		ip = entry[1]
		typeOfInterface = entry[2]
		name = constructName(entry[3])
		# construct IP lookup
		if ip in ipToName:
			duplicateIPs.add(ip)
		else:
			ipToName[ip] = name
			if keepRecords:
				ipToRecord[ip] = dnsRecord
		# construct name lookup
		if name in nameToIPs:
			nameToIPs[name].add(ip)
		else:
			nameToIPs[name] = set([ip])


	return (ipToName, nameToIPs, duplicateIPs, ipToRecord)


# Get Cisco model from abbrevation
# Map from: http://cpansearch.perl.org/src/KBRINT/Cisco-Abbrev-0.02/lib/Cisco/Abbrev.pm
#
# Juniper listing: http://www.juniper.net/techpubs/software/junos-security/junos-security10.0/junos-security-swconfig-interfaces-and-routing/network-interfaces-section.html
def get_model(model_abbr):
	abbreviations = {
		'fa': 'FastEthernet',
		'gi': 'GigabitEthernet',
		'te': 'TenGigabitEthernet',
		'et': 'Ethernet',
		'vl': 'Vlan',
		'fd': 'Fddi',
		'is': 'IntegratedServicesModule',
		#'portch': 'Port-channel',
		#'po': 'Port-channel',

		'tu': 'Tunnel',
		'lo': 'Loopback',
		'vi': 'Virtual-Access',
		'vt': 'Virtual-Template',
		'eo' : 'EOBC',

		'se': 'Serial',
		'Se': 'Serial',
		'po': 'POS',
		'posch': 'Pos-channel',
		'mu': 'Multilink',
		'at': 'ATM',

		'async': 'Async',
		'group-async': 'Group-Async',
		'mfr': 'MFR'
	}

	try:
		return abbreviations[model_abbr]
	except KeyError:
		return "(unknown)"

	
"""
Stolen entry reconstruction function from pl_bin/sort-atlas.py
"""
def getMasterAtlasEntry(ip, dnsRecord):

	toreturn = ""
	
	# get model for this record
	model = get_model(dnsRecord[0:2])
	if dnsRecord[0:4] == "giga":
		model = "(unknown)"
	if dnsRecord[0:3] == "tel":
		model = "(unknown)"
	if dnsRecord[0:3] == "isc":
		model = "(unknown)"
	if dnsRecord[0:3] == "att":
		model = "(unknown)"

	# save broken up record
	tmp = dnsRecord[:-2].split(".")[:-3]
	tmp.reverse()
	for part in tmp:
		toreturn += part + "\t"
	
	if len(tmp) < 3:
		toreturn += "\t"

	toreturn += dnsRecord[:-2] + "\t"
	toreturn += ip + "\t"
	toreturn += model

	return toreturn



def main():

	# parse command line options
	dnsRecordsFilename = None
	outputDirFilename = None
	if len(sys.argv) == 2:
		dnsRecordsFilename = sys.argv[1]
		outputDirFilename = dnsRecordsFilename
	elif len(sys.argv) == 3:
		dnsRecordsFilename = sys.argv[1]
		outputDirFilename = sys.argv[2]
	else:
		print "Usage: " + sys.argv[0] + " dnsRecords [outputDirectory]"
		print "Note: If outputDirectory is specified, then all the weeks data will be\n" \
		"reconstructed in that directory. Otherwise the will be placed in the dnsRecords directory."
		sys.exit(1)

	# check that output dir exists
	if not os.path.exists(outputDirFilename):
		os.makedirs(outputDirFilename)
	
	try:
		# get weeks
		weeks = []
		for week in os.listdir(dnsRecordsFilename):
			try:
				# take only directories that are numbers
				weeks.append(int(week))
			except ValueError:
				sys.stderr.write("Directory/file \"" + week + "\"" \
						"is not a week number as expected\n")
				continue
		weeks = sorted(weeks)

		# just copy edge weeks for consistency
		for currWeek in [weeks[0], weeks[-1]]:
			# get directory create fixed file in
			outputWeekDirFilename = outputDirFilename + "/" + str(currWeek)
			if not os.path.exists(outputWeekDirFilename):
				os.makedirs(outputWeekDirFilename)
			
			# delete any old versions of this file
			outputFilename = outputWeekDirFilename + "/" + fixedFilename
			if os.path.exists(outputFilename):
				os.remove(outputFilename)

			# copy the original file to start appending to
			currWeekFilename = dnsRecordsFilename + "/" + str(currWeek) + "/COGENT-MASTER-ATLAS.txt"
			shutil.copy(currWeekFilename, outputFilename)

		# chop off ends so that we can always analyze surrouding weeks	
		weeks = weeks[1:-1]
		
		# iterate over weeks and look for anomalies
		for weekN in weeks:
			try:
				# get weeks
				#NOTE: Results are a tuple (ipToName, nameToIPs, duplicateIPs, ipToRecord)
				prevWeek = weekN - 1
				prevWeekFilename = dnsRecordsFilename + "/" + str(prevWeek) + "/COGENT-MASTER-ATLAS.txt"
				prevWeekFile = open(prevWeekFilename, "r")
				prevWeekResults = parseDNSRecords(prevWeekFile, True)

				currWeek = weekN
				currWeekFilename = dnsRecordsFilename + "/" + str(currWeek) + "/COGENT-MASTER-ATLAS.txt"
				currWeekFile = open(currWeekFilename, "r")
				currWeekResults = parseDNSRecords(currWeekFile, False)

				nextWeek = weekN + 1
				nextWeekFilename = dnsRecordsFilename + "/" + str(nextWeek) + "/COGENT-MASTER-ATLAS.txt"
				nextWeekFile = open(nextWeekFilename, "r")
				nextWeekResults = parseDNSRecords(nextWeekFile, False)

				# find missing IPs
				ipToRecords = prevWeekResults[3]
				prevIPs = set(prevWeekResults[0].keys())
				currIPs = set(currWeekResults[0].keys())
				nextIPs = set(nextWeekResults[0].keys())
				ipsInPrevAndNext = prevIPs & nextIPs
				ipsMissingInCurr = ipsInPrevAndNext - currIPs

				# classify missing IPs into one of three cases:
				# 1. IP has same DNS record in prev and next
				# OR IP has different DNS record and:
				#	2. DNS record from prev belongs to other IPs
				#	3. DNS record from prev has disappeared 
				case1IPs = [] # list of tuples (ip, bothDNSrecord)
				case2IPs = [] # list of tuples (ip, prevDNSrecord, nextDNSrecord, prevIPs, nextIPs)
				case3IPs = [] # list of tuples (ip, prevDNSrecord, nextDNSrecord)
				for ip in ipsMissingInCurr:
					prevDNS = prevWeekResults[0][ip]
					nextDNS = nextWeekResults[0][ip]
					# case 1
					if prevDNS == nextDNS:
						case1IPs.append((ip, prevDNS))
					else:
						try:
							# case 2
							prevIPs = prevWeekResults[1][prevDNS]
							nextIPs = nextWeekResults[1][prevDNS]
							case2IPs.append((ip, prevDNS, nextDNS, prevIPs, nextIPs))
						except KeyError:
							# case 3
							case3IPs.append((ip, prevDNS, nextDNS))

				# output results

				# get directory create fixed file in
				outputWeekDirFilename = outputDirFilename + "/" + str(currWeek)
				if not os.path.exists(outputWeekDirFilename):
					os.makedirs(outputWeekDirFilename)
				
				# delete any old versions of this file
				outputFilename = outputWeekDirFilename + "/" + fixedFilename
				if os.path.exists(outputFilename):
					os.remove(outputFilename)

				# copy the original file to start appending to
				shutil.copy(currWeekFilename, outputFilename)
				
				# write case 1s to appended file
				with open(outputFilename, "a") as outputFile:
					for entry in case1IPs:
						ip = entry[0]
						outputFile.write(getMasterAtlasEntry(ip, ipToRecords[ip]) + "\n")

			except:
				raise
				sys.stderr.write("Skipping week " + str(weekN) + "\n")

	except:
		raise
		print "Error: Could not open \"" + dnsRecordsFilename + "\""
		sys.exit(1)


if __name__ == "__main__":
	main()
