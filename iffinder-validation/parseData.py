#!/usr/bin/python

#TODO: What additional sanity checks do we need?
#	-Use pl_bin/sort-atlas.py as inspiration to split router interfaces into physical and non-physical
#	-Reverse DNS record similarities
#	-Cross-reference week by week to build more complete graph, use DNS records to ensure it was just returned
#	ip that changed and not 
#	- We're more interested in statistics

#TODO: Graph edge analysis?
#	-/30 blocks should be connected by a link
#	-Traceroute shows connections

import sys
import re


"""
Constructs a name from a list of subdomains gathered from DNS queries.
"""
def constructName(nameList):
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

Then, these tuples are loaded into an IP -> ([subdomains], type of interface)
dictionary and a location-subdomain -> IP dictionary

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
	
	for entry in parsed:
		ip = entry[1]
		typeOfInterface = entry[2]
		name = constructName(entry[3])
		# construct IP lookup
		if ip in ipToName:
			sys.stderr.write("IP " + ip + " found twice!\n")
		else:
			ipToName[ip] = (name, typeOfInterface)
		#construct name lookup
		if name in nameToIPs:
			nameToIPs[name].add((ip, typeOfInterface))
		else:
			nameToIPs[name] = set([(ip, typeOfInterface)])

	return ipToName, nameToIPs
		

"""
Reads iffinder content and parse it into tuples structured as follows:

	(addr, alias, o-TTL-r, RTT, result)

Then, these tuples are checked for similarity and lists of addrs are
calculated such that each list contains IPs which are believed to belong
to interfaces on the same router.
"""
def parseIffinderResults(source):
	# parse the file into usable tuples
	parsed = []
	for line in source.readlines():
		# check if line is a comment
		if line[0] == "#":
			continue

		# try and parse line
		splitLine = re.split("\s+", line.strip())
		if len(splitLine) == 8:
			addr = splitLine[0]
			alias = splitLine[1]
			oTTLr = (splitLine[2], splitLine[3])
			RTT = splitLine[4]
			iffResult = splitLine[5]
			theTuple = (addr, alias, oTTLr, RTT, iffResult)
			parsed.append(theTuple)
		else:
			continue

	# next router ID to give out
	nextRouterID = 0
	# { router ID -> set(interface IPs) }
	routerToIPs = {}
	# { interface IP -> router ID }
	ipToRouter = {}


	# load candidates based on aliases responses
	for entry in parsed:
		addr = entry[0]
		alias = entry[1]
		result = entry[4]

		# only use this parsed entry if it successfully elicited a response
		if result != "D" and result != "S":
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

	return (routerToIPs, ipToRouter)


"""
Given the iffinder results and DNS results, find named routers and their corresponding IPs
"""
def combineIPDictionaries(ipToRouter, ipToName):
	# dictionary to hold a name with all the ips associated with that name
	namedRouterToIPs = {}
	# dictionary of router IDs from iffinder to names, used to check accuracy of data
	nameToRouter = {}
	# counter of how many times we find analysis disagreements
	disagreements = 0
	for ip in ipToRouter:
		if ip in ipToName:
			router = ipToRouter[ip]
			name = ipToName[ip]
			# check if we've seen this name before
			if name in nameToRouter:
				# check if iffinder and dns records agree
				previousRouter = nameToRouter[name]
				if router != previousRouter:
					sys.stderr.write("iffinder found IP " + ip + \
							" in router " + str(router) + \
							" but DNS records say it should belong to router " \
							+ str(previousRouter) + "\n")
					disagreements += 1
			else:
				nameToRouter[name] = router
			# combine data into named routers
			# TODO: How should we do this? Right now I am essentially copying the nameToIPs dictionary
			if name in namedRouterToIPs:
				namedRouterToIPs[name].add(ip)
			else:
				namedRouterToIPs[name] = set([ip])
	return (namedRouterToIPs, disagreements)


"""
               _       _         _             _         _                   
 ___  ___ _ __(_)_ __ | |_   ___| |_ __ _ _ __| |_ ___  | |__   ___ _ __ ___ 
/ __|/ __| '__| | '_ \| __| / __| __/ _` | '__| __/ __| | '_ \ / _ \ '__/ _ \
\__ \ (__| |  | | |_) | |_  \__ \ || (_| | |  | |_\__ \ | | | |  __/ | |  __/
|___/\___|_|  |_| .__/ \__| |___/\__\__,_|_|   \__|___/ |_| |_|\___|_|  \___|
                |_|                                                          
"""
# parse command line options
if len(sys.argv) != 3:
	print "Usage: " + sys.argv[0] + " iffinderResults dnsRecords"
	sys.exit(1)
try:
	iffinderResults = open(sys.argv[1], "r")
	dnsRecords = open(sys.argv[2], "r")
except:
	print "Error: Could not open one or more of the specified files."
	sys.exit(1)

# do analysis
routerToIPs, ipToRouter = parseIffinderResults(iffinderResults)
ipToName, nameToIPs = parseDNSRecords(dnsRecords)

# sanity check data
iffinderIPs = set(ipToRouter.keys())
dnsRecordIPs = set(ipToName.keys())
ipDifference = iffinderIPs ^ dnsRecordIPs
for ip in ipDifference:
	sys.stderr.write("Found IP " + ip + " in either iffinder or dns records but not in both.\n")

# combine data
namedRouterToIPs, disagreements = combineIPDictionaries(ipToRouter, ipToName)

# begin stats
sys.stderr.write("-----------------\n")

# print iffinder statistic to stderr
numRouters = len(routerToIPs.keys())
numInterfaces = map(len, routerToIPs.values())
avgInterfaces = sum(numInterfaces)/numRouters
sys.stderr.write("iffinder results:\n")
sys.stderr.write("\tNumber of routers found: " + str(numRouters) + "\n")
sys.stderr.write("\tNumber of addrs to aliases:\n\t\tAvg: " + str(avgInterfaces) + "\n\t\tMax: " + str(max(numInterfaces)) + "\n\t\tMin: " + str(min(numInterfaces)) + "\n")

# print dns record statistics to stderr
numNames = len(nameToIPs.keys())
numInterfaces = map(len, nameToIPs.values())
avgInterfaces = sum(numInterfaces)/numNames
sys.stderr.write("dns record results:\n")
sys.stderr.write("\tNumber of names found: " + str(numNames) + "\n")
sys.stderr.write("\tNumber of IPs to names:\n\t\tAvg: " + str(avgInterfaces) + "\n\t\tMax: " + str(max(numInterfaces)) + "\n\t\tMin: " + str(min(numInterfaces)) + "\n")

# print combined output
sys.stderr.write("Disagreements between iffinder and dns records: " + str(disagreements) + " (" + str(int(disagreements/(1.0 * len(ipToName)) * 100.0)) + "% of total)\n")

# end stats
sys.stderr.write("-----------------\n")

# print router information to stdout
for name in namedRouterToIPs:
	print str(name) + " -> " + str(sorted(namedRouterToIPs[name]))
