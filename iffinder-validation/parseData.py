#!/usr/bin/python
"""
Reads iffinder content and parse it into tuples structured as follows:

	(addr, alias, o-TTL-r, RTT, result)

Then, these tuples are checked for similarity and lists of addrs are
calculated such that each list contains IPs which are believed to belong
to interfaces on the same router.
"""
import sys
import re

# parse the file into usable tuples
parsed = []
for line in sys.stdin.readlines():
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


#TODO: What additional sanity checks do we need?
#	-Use pl_archives to cross-reference IPs with dns records for determining interface type and location
#	-Use pl_bin/sort-atlas.py as inspiration to split router interfaces into physical and non-physical
#	-Reverse DNS record similarities
#	-Cross-reference week by week to build more complete graph, use DNS records to ensure it was just returned
#	ip that changed and not 
#	-Find situations where DNS and iffinder do not agree, these are situations where a new router was installed
#	and DNS were not kept up to date.
#	- We're more interested in statistics

#TODO: Graph edge analysis?
#	-/30 blocks should be connected by a link
#	-Traceroute shows connections

# sanity check results by ensuring every IP belongs to exactly one router
allIPs = set()
for router in routerToIPs:
	for ip in routerToIPs[router]:
		if ip in allIPs:
			sys.stderr.write("IP " + ip + " already found!\n")
		else::w
			allIPs.add(ip)


# print statistic to stderr
numParsed = len(parsed)
numRouters = len(routerToIPs.keys())
numInterfaces = map(len, routerToIPs.values())
avgInterfaces = sum(numInterfaces)/numRouters
sys.stderr.write("Number of lines parsed: " + str(numParsed) + "\n")
sys.stderr.write("Number of routers found: " + str(numRouters) + " (" + str(int((numRouters / (1.0 * numParsed)) * 100)) +"% of parsed)\n")
sys.stderr.write("Number of addrs to aliases:\n\tAvg: " + str(avgInterfaces) + "\n\tMax: " + str(max(numInterfaces)) + "\n\tMin: " + str(min(numInterfaces)) + "\n")

# print router information to stdout
for router in routerToIPs:
	print "Router " + str(router) + " -> " + str(sorted(routerToIPs[router]))
