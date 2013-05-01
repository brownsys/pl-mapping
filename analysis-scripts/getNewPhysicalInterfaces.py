#!/usr/bin/python
"""
This script looks for new physical interfaces in the iffinder/DNS data from week to week.
It specifically looks for physical interface IPs which appear in week N-1, not in week N, and
then again in week N+1. It prints results to stdout.
"""
import sys
import re
import operator
import os
from routerInterfaces import getBreakdown

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
			ipToName[ip] = name
		#construct name lookup
		if name in nameToIPs:
			nameToIPs[name].add(ip)
		else:
			nameToIPs[name] = set([ip])


	return (ipToName, nameToIPs, duplicateIPs)
		
def main():
	weeks = None

	# parse command line options
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " dnsRecords [weekNumbers]"
		print "Options:"
		print "\t[weekNumbers] are white-space separated weeks of interest"
		sys.exit(1)
	elif len(sys.argv) > 2:
		for option in sys.argv[2:]:
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

		# iterate over weeks and look for anomalies
		print "# Week\tNumNewPhyInterfaces"
		for weekN in weeks:
			try:
				# get weeks
				#NOTE: Results are a tuple (ipToName, nameToIPs, duplicateIPs)
				prevWeek = weekN - 1
				prevWeekFilename = dnsRecordsFilename + "/" + str(prevWeek) + "/COGENT-MASTER-ATLAS.txt"
				prevWeekFile = open(prevWeekFilename, "r")
				prevWeekResults = parseDNSRecords(prevWeekFile)
				prevWeekFile.close()	
				prevWeekFile = open(prevWeekFilename, "r")
				prevPhysicalInterfaces, _, _ = getBreakdown(prevWeekFile)

				currWeek = weekN
				currWeekFilename = dnsRecordsFilename + "/" + str(currWeek) + "/COGENT-MASTER-ATLAS.txt"
				currWeekFile = open(currWeekFilename, "r")
				currWeekResults = parseDNSRecords(currWeekFile)
				currWeekFile.close()	
				currWeekFile = open(currWeekFilename, "r")
				currPhysicalInterfaces, _, _ = getBreakdown(currWeekFile)

				# find new IPs
				prevIPs = set(filter(lambda x: x in prevPhysicalInterfaces, prevWeekResults[0].keys()))
				currIPs = set(filter(lambda x: x in currPhysicalInterfaces, currWeekResults[0].keys()))
				newIPs = currIPs - prevIPs

				# print count
				print str(currWeek) + "\t" + str(len(newIPs))
			except:
				raise
				sys.stderr.write("Skipping week " + str(weekN) + "\n")

	except:
		raise
		print "Error: Could not open \"" + dnsRecordsFilename + "\""
		sys.exit(1)


if __name__ == "__main__":
	main()
