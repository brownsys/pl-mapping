#!/usr/bin/python
"""
This script looks for anomalies in the iffinder/DNS data from week to week.
It specifically looks for IPs which appear in week N-1, not in week N, and
then again in week N+1. It prints anomalies to stdout.
"""
import sys
import re
import operator
import os

# determines how strict we should be about the DNS record names.
#
# if set to True, we consider these interfaces to be on the same router:
#     gi1-38.3504.ccr01.jfk03.atlas.cogentco.com
#     gi1-43.3501.ccr01.jfk03.atlas.cogentco.com
# by dropping "3504" and "3501" respectively from each interface name

nonStrictNames = True

onlyDisappeared = False
detailed = False
raw = False

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
def parseDNSRecords(source):
	# parse the file into usable tuples
	parsed = []
	for line in source.readlines():
		splitLine = re.split("\s+", line.strip())
		parsed.append((splitLine[-3], splitLine[-2], splitLine[-1], splitLine[:-3][::-1]))

	# build dictionaries
	ipToName = {}
	nameToIPs = {}
	duplicateIPs = set()
	
	for entry in parsed:
		ip = entry[1]
		typeOfInterface = entry[2]
		name = constructName(entry[3])
		# construct IP lookup
		if ip in ipToName:
			duplicateIPs.add(ip)
		else:
			#ipToName[ip] = (name, typeOfInterface)
			ipToName[ip] = name
		#construct name lookup
		if name in nameToIPs:
			#nameToIPs[name].add((ip, typeOfInterface))
			nameToIPs[name].add(ip)
		else:
			#nameToIPs[name] = set([(ip, typeOfInterface)])
			nameToIPs[name] = set([ip])


	return (ipToName, nameToIPs, duplicateIPs)
		
def main():
	global onlyDisappeared
	global detailed
	global raw
	weeks = None

	# parse command line options
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " dnsRecords [weekNumbers] [options]"
		print "Options:"
		print "\t[weekNumbers] are white-space separated weeks of interest"
		print "\t--onlyDisappeared\tonly show IPs that disappear for a week"
		print "\t--detailed\tprint information about how DNS records change"
		print "\t--raw\tprints ouput with minimal text (does not work with detailed)"
		sys.exit(1)
	elif len(sys.argv) > 2:
		for option in sys.argv[2:]:
			if option == "--onlyDisappeared":
				onlyDisappeared = True
			if option == "--detailed":
				detailed = True
			if option == "--raw":
				raw = True
			else:
				try:
					aweek = int(option)
					if weeks == None:
						weeks = [aweek]
					else:
						weeks.append(aweek)
				except ValueError:
					continue

	dnsRecordsFilename = sys.argv[1]
		
	try:
		# get weeks if didn't get them from the options
		if weeks == None:
			weeks = []
			for week in os.listdir(dnsRecordsFilename):
				try:
					# take only directories that are numbers
					weeks.append(int(week))
				except ValueError:
					sys.stderr.write("Directory/file \"" + week + "\"" \
							"is not a week number as expected\n")
					continue
			# sort weeks and chop off ends so we don't index poorly
			weeks = sorted(weeks)
			weeks = weeks[1:-1]

		# stats
		numCase1 = 0
		numCase2 = 0
		numCase3 = 0
		
		# iterate over weeks and look for anomalies
		for weekN in weeks:
			try:
				# get weeks
				#NOTE: Results are a tuple (ipToName, nameToIPs, duplicateIPs)
				prevWeek = weekN - 1
				prevWeekFilename = dnsRecordsFilename + "/" + str(prevWeek) + "/COGENT-MASTER-ATLAS.txt"
				prevWeekFile = open(prevWeekFilename, "r")
				prevWeekResults = parseDNSRecords(prevWeekFile)

				currWeek = weekN
				currWeekFilename = dnsRecordsFilename + "/" + str(currWeek) + "/COGENT-MASTER-ATLAS.txt"
				currWeekFile = open(currWeekFilename, "r")
				currWeekResults = parseDNSRecords(currWeekFile)

				nextWeek = weekN + 1
				nextWeekFilename = dnsRecordsFilename + "/" + str(nextWeek) + "/COGENT-MASTER-ATLAS.txt"
				nextWeekFile = open(nextWeekFilename, "r")
				nextWeekResults = parseDNSRecords(nextWeekFile)

				# find missing IPs
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

				# print Case 1 results
				if raw:
					print "# Case 1"
					print "# IP\tWeek\tDNS Record"
				for entry in case1IPs:
					if raw:
						print entry[0] + "\t" + str(currWeek) + "\t" + entry[1]
					else:
						print "IP " + entry[0] + " has record " + entry[1] + " in weeks " + str(prevWeek) + " and " + str(nextWeek) + \
								" but does not appear in week " + str(currWeek)

				if not onlyDisappeared:

					# print Case 2 results
					if raw:
						print "# Case 2"
						print "# IP\tWeek\tPrev Record\tNext Record"
					for entry in case2IPs:
						if raw:
							print entry[0] + "\t" + str(currWeek) + "\t" + entry[1] + "\t" + entry[2]
						else:
							print "IP " + entry[0] + " has record " + entry[1] + " in week " + str(prevWeek) + ", does not appear in week " \
									+ str(currWeek) + " and has record " + entry[2] + " in week " + str(nextWeek)
							if detailed:
								print "Record " + entry[1] + " has IPs " + str(entry[3]) + " in week " + str(prevWeek) + " but has IPs " + \
										str(entry[4]) + " in week " + str(nextWeek)

					# print Case 3 results
					if raw:
						print "# Case 3"
						print "# IP\tWeek\tPrev Record\tNext Record"
					for entry in case3IPs:
						if raw:
							print entry[0] + "\t" + str(currWeek) + "\t" + entry[1] + "\t" + entry[2]
						else:
							print "IP " + entry[0] + " has record " + entry[1] + " in week " + str(prevWeek) + ", does not appear in week " \
									+ str(currWeek) + " and has record " + entry[2] + " in week " + str(nextWeek)
							if detailed:
								print "Record " + entry[1] + " from week " + str(prevWeek) + " disappears in week " + str(nextWeek)

				# collect stats
				numCase1 += len(case1IPs)
				numCase2 += len(case2IPs)
				numCase3 += len(case3IPs)
			except:
				raise
				sys.stderr.write("Skipping week " + str(weekN) + "\n")

	except:
		raise
		print "Error: Could not open \"" + dnsRecordsFilename + "\""
		sys.exit(1)

	# print stats
	sys.stderr.write("Number of case 1s: " + str(numCase1) + "\n")
	sys.stderr.write("Number of case 2s: " + str(numCase2) + "\n")
	sys.stderr.write("Number of case 3s: " + str(numCase3) + "\n")

if __name__ == "__main__":
	main()
