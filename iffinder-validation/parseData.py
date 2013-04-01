#!/usr/bin/python

#TODO: What additional sanity checks do we need?
#	-Use pl_bin/sort-atlas.py as inspiration to split router interfaces into physical and non-physical
#	-Reverse DNS record similarities
#	-Cross-reference week by week to build more complete graph, use DNS records to ensure it was just returned
#	ip that changed and not 
#	- We're more interested in statistics
#	-Airports folder, output.txt, cogent_airport_codes

#TODO: Graph edge analysis?
#	-/30 blocks should be connected by a link
#	-Traceroute shows connections

#TODO: Questions about the data?
#	-Certain IPs were discovered by iffinder, why weren't they in the original list of IPs?
#		-They have no reverse DNS records, print a count of the IPs which have this
#	-Why are the multiple DNS records per IP? Ex: In week 1, 66.250.250.122 has two reverse DNS records

import sys
import re
import operator

# determines how strict we should be about the DNS record names.
nonStrictNames = False

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
	if len(nameList) >= 3:
		typeOfInterface = nameList[0]
		location = nameList[1]
		routerIdentifier = nameList[2]
		return ".".join([location, routerIdentifier])
	else:
		return ".".join(nameList)

"""
Read reverse DNS records and parse it into tuples structured as follows:

	(domain, IP, type of interface, [subdomains])

DEPRECATED COMMENT: Then, these tuples are loaded into an IP -> ([subdomains], type of interface)
dictionary and a location-subdomain -> IP dictionary

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
		

"""
Reads iffinder content and parse it into tuples structured as follows:

	(addr, alias, o-TTL-r, RTT, result, discover)

Then, these tuples are checked for similarity and lists of addrs are
calculated such that each list contains IPs which are believed to belong
to interfaces on the same router.
"""
def parseIffinderResults(source):
	# parse the file into usable tuples
	parsed = []
	for line in source.readlines():
		# check if line is a comment
		if line[0] == "#" or line.find("skipping") != -1:
			continue

		# try and parse line
		splitLine = re.split("\s+", line.strip())
		if len(splitLine) == 8:
			addr = splitLine[0]
			alias = splitLine[1]
			oTTLr = (splitLine[2], splitLine[3])
			RTT = splitLine[4]
			iffResult = splitLine[5]
			discover = splitLine[6]
			theTuple = (addr, alias, oTTLr, RTT, iffResult, discover)
			parsed.append(theTuple)
		else:
			continue

	# next router ID to give out
	nextRouterID = 0
	# { router ID -> set(interface IPs) }
	routerToIPs = {}
	# { interface IP -> router ID }
	ipToRouter = {}
	# set of unsuccessful IPs 
	unsuccessfulIPs = set()
	# set of discovered IPs
	discoveredIPs = set()

	# load candidates based on aliases responses
	for entry in parsed:
		addr = entry[0]
		alias = entry[1]
		result = entry[4]
		discover = entry[5]

		shouldContinue = False

		# only use this parsed entry if it successfully elicited a response
		if result != "D" and result != "S":
			unsuccessfulIPs.add(addr)
			shouldContinue = True

		# check if this ip was discovered
		if discover != "-":
			discoveredIPs.add(addr)
			shouldContinue = True

		if shouldContinue:
			continue

		# we've seen both these IPs before
		if addr in ipToRouter and alias in ipToRouter:
			addrRouter = ipToRouter[addr]
			aliasRouter = ipToRouter[alias]
			# if we don't think these two IPs are on the same router
			# then join them into one router
			if addrRouter != aliasRouter:
				# we'll use the addr router as the combined router ID
				# update the routerToIPs mapping
				routerToIPs[addrRouter] = routerToIPs[addrRouter].union(routerToIPs[aliasRouter])
				# update the ipToRouter mapping
				for ip in routerToIPs[aliasRouter]:
					ipToRouter[ip] = addrRouter
				# delete old router
				del routerToIPs[aliasRouter]
			# we already knew these were on the same router
			else:
				continue
		# we've seen the addr IP before but not alias IP
		elif addr in ipToRouter:	
			addrRouter = ipToRouter[addr]
			# update the routerToIPs mapping
			routerToIPs[addrRouter].add(alias)
			# update the ipToRouter mapping
			ipToRouter[alias] = addrRouter
		# we've seen the alias IP before but not addr IP
		elif alias in ipToRouter:
			aliasRouter = ipToRouter[alias]
			# update the routerToIPs mapping
			routerToIPs[aliasRouter].add(addr)
			# update the ipToRouter mapping
			ipToRouter[addr] = aliasRouter
		# wev've never seen either IP before
		else:
			# get new router ID
			newRouter = nextRouterID
			nextRouterID += 1
			# update the routerToIPs mapping
			routerToIPs[newRouter] = set([addr, alias])
			# update the ipToRouter mapping
			ipToRouter[addr] = newRouter
			ipToRouter[alias] = newRouter

	return (routerToIPs, ipToRouter, unsuccessfulIPs, discoveredIPs)

"""
Returns a dictionary of names to numbers of votes
"""
def getVotes(routerIPs, ipToName):
	votes = {}
	for ip in routerIPs:
		name = ipToName[ip]
		if name in votes:
			votes[name] += 1
		else:
			votes[name] = 1
	return votes

"""
Returns a sorted list of the most popular router as voted by you, the DNS records,
"""
def analyzeVotes(votes):
	analysis = sorted(votes.items(), key=operator.itemgetter(1), reverse=True)
	analyzed = map(lambda x:x[0], analysis)
	#sys.stderr.write("analyzed: " + str(analyzed) + "\n")
	return analyzed 


"""
Returns IPs whose names match voted names in set and
a dictionary of names to all other IPs
"""
def getMajorityAndMinority(routerIPs, ipToName, mostPopularName):
	minorityIPs = {}
	majorityIPs = set()
	for ip in routerIPs:
		name = ipToName[ip]
		if name == mostPopularName:
			majorityIPs.add(ip)
		else:
			if name in minorityIPs:
				minorityIPs[name].add(ip)
			else:
				minorityIPs[name] = set([ip])
	return (majorityIPs, minorityIPs)

"""
Given the iffinder results and DNS results, find named routers and their corresponding IPs
"""
def combineIPDictionaries(routerToIPs, ipToName):
	# dictionary to hold a name with all the ips associated with that name
	# the IPs in here are all confirmed by iffinder
	namedRouterToIPs = {}
	# IPs that didn't vote with the majority are kept in a dictionary
	# of tuple keys (DNS name, iffinder majority name) to IPs
	outlierToIPs = {}
	# counter of how many times we find votes aren't unanimous
	notUnanimous = 0
	
	# iterate over iffinder defined router
	for routerID in routerToIPs:
		routerIPs = routerToIPs[routerID] & set(ipToName.keys())
		if len(routerIPs) == 0:
			continue
		"""
		for ip in routerIPs:
			if ip not in ipToName:
				sys.stderr.write("IP " + ip + " not found in ipToName?\n")
		"""
		
		# check if the votes are unanimous
		votes = getVotes(routerIPs, ipToName)
		votedNames = analyzeVotes(votes)
		mostPopularName = votedNames[0]
		if len(votes.keys()) == 1:
			if mostPopularName in namedRouterToIPs:
				namedRouterToIPs[mostPopularName].update(routerIPs)
			else:
				namedRouterToIPs[mostPopularName] = set(routerIPs)
		else:
			notUnanimous += 1
			majorityIPs, minorityIPs = getMajorityAndMinority(routerIPs, ipToName, mostPopularName)
			# add majority IPs to router
			if mostPopularName in namedRouterToIPs:
				namedRouterToIPs[mostPopularName].update(majorityIPs)
			else:
				namedRouterToIPs[mostPopularName] = set(majorityIPs)
			# add minority IPS to outlier
			for name in minorityIPs:
				key = (name, mostPopularName)
				if key in outlierToIPs:
					outlierToIPs[key].update(minorityIPs[name])
				else:
					outlierToIPs[key] = set(minorityIPs[name])

	return (namedRouterToIPs, outlierToIPs, notUnanimous)

"""
               _       _         _             _         _                   
 ___  ___ _ __(_)_ __ | |_   ___| |_ __ _ _ __| |_ ___  | |__   ___ _ __ ___ 
/ __|/ __| '__| | '_ \| __| / __| __/ _` | '__| __/ __| | '_ \ / _ \ '__/ _ \
\__ \ (__| |  | | |_) | |_  \__ \ || (_| | |  | |_\__ \ | | | |  __/ | |  __/
|___/\___|_|  |_| .__/ \__| |___/\__\__,_|_|   \__|___/ |_| |_|\___|_|  \___|
                |_|                                                          
"""
# parse command line options
if len(sys.argv) != 3 and len(sys.argv) != 4:
	print "Usage: " + sys.argv[0] + " iffinderResults dnsRecords [nonStrictNames]"
	sys.exit(1)
try:
	iffinderResults = open(sys.argv[1], "r")
	dnsRecords = open(sys.argv[2], "r")
	nonStrictNames = False
	if len(sys.argv) == 4:
		nonStrictNames = True
except:
	print "Error: Could not open one or more of the specified files."
	sys.exit(1)

# do analysis
routerToIPs, ipToRouter, unsuccessfulIPs, discoveredIPs = parseIffinderResults(iffinderResults)
ipToName, nameToIPs, duplicateIPs = parseDNSRecords(dnsRecords)	

"""
print "---------------------routerToIPs----------------------------"
print routerToIPs
print "---------------------ipToRouter----------------------------"
print ipToRouter
print "---------------------unsuccessfulIPs-------------------------"
print unsuccessfulIPs
print "---------------------ipToName-------------------------------"
print ipToName
print "-----------------------nameToIPs---------------------------"
print nameToIPs
"""

# combine data
namedRouterToIPs, outlierToIPs, notUnanimous = combineIPDictionaries(routerToIPs, ipToName)

# begin stats
sys.stderr.write("-----------------\n")

# print iffinder statistic to stderr
numRouters = len(routerToIPs.keys())
numUnsuccessful = len(unsuccessfulIPs)
numDiscovered = len(discoveredIPs)
numInterfaces = map(len, routerToIPs.values())
avgInterfaces = sum(numInterfaces)/numRouters
sys.stderr.write("iffinder results:\n")
sys.stderr.write("\tNumber of routers found: " + str(numRouters) + "\n")
sys.stderr.write("\tNumber of non-responsive IPs: " + str(numUnsuccessful) + "\n")
sys.stderr.write("\tNumber of discover IPs: " + str(numDiscovered) + "\n")
sys.stderr.write("\tNumber of addrs to aliases:\n\t\tAvg: " + str(avgInterfaces) + "\n\t\tMax: " + str(max(numInterfaces)) + "\n\t\tMin: " + str(min(numInterfaces)) + "\n")

# print dns record statistics to stderr
numNames = len(nameToIPs.keys())
numDuplicateIPs= len(duplicateIPs)
numInterfaces = map(len, nameToIPs.values())
avgInterfaces = sum(numInterfaces)/numNames
sys.stderr.write("dns record results:\n")
sys.stderr.write("\tNumber of names found: " + str(numNames) + "\n")
sys.stderr.write("\tNumber of ips with multiple reverse DNS records: " + str(numDuplicateIPs) + "\n")
sys.stderr.write("\tNumber of IPs to names:\n\t\tAvg: " + str(avgInterfaces) + "\n\t\tMax: " + str(max(numInterfaces)) + "\n\t\tMin: " + str(min(numInterfaces)) + "\n")

# print combined output
sys.stderr.write("Non-unanimous agreement in iffinder and dns record analysis: " + str(notUnanimous) + " (" + str(int(notUnanimous/(1.0 * len(routerToIPs)) * 100.0)) + "% of total)\n")

# end stats
sys.stderr.write("-----------------\n")

# print router information to stdout
print "# Named routers as determined by iffinder and reverse DNS records"
print "# Name\tIPs"
for name in namedRouterToIPs:
	print str(name) + "\t" + str(sorted(namedRouterToIPs[name]))
print "# Iffinder/DNS Disagreements"
print "# DNS Name\tiffinder Name\tIPs"
for outlier in outlierToIPs:
	print str(outlier[0]) + "\t" + str(outlier[1]) + "\t" + str(sorted(outlierToIPs[outlier]))
