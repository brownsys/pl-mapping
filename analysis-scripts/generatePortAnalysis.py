#!/usr/bin/python
"""
Get a summary of how many modules are used per router and how many ports are used per module.

Data is output in the following format.

Avg Modules/Router: x
Max Modules/Router: x
Avg Port Density/Module: x
"""

import os
import sys
import re

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
Takes in a COGENT-MASTER-ATLAS-FIXED.txt file for a week and
reads it to parse it into router. Returns a list of lists
where each sublist contains the DNS records for a single router
and a count of how many DNS records could not be used because
they were not structured as expected.
"""
def getRouters(masterAtlas):
	routerToDNS = {}
	totalCount = 0
	skipCount = 0

	# iterate through entries in file
	for line in masterAtlas.readlines():
		# split line into usuable chunks
		splitLine = re.split("\s+", line.strip());
		
		# get relevant information
		routerName = constructName(splitLine[:-3][::-1]) # group DNS records which belong to the same router
		portSubstring = splitLine[-4] # this string will contain the module and port information

		# only use substrings with a dash since these contain information we are interested in
		totalCount += 1
		if portSubstring.find('-') == -1:
			skipCount += 1
			continue

		# build up our lists
		if routerName in routerToDNS:
			routerToDNS[routerName].append(portSubstring[2:])
		else:
			routerToDNS[routerName] = [portSubstring[2:]]

	return routerToDNS, totalCount, skipCount


"""
Takes a list of "module-port" strings belonging to a single router.
Return a dictionary of modules to the ports used on these module.
"""
def getModules(router):
	# dictionary maps module number to set of port numbers
	moduleToPorts = {}

	# iterate over a router's records
	for record in router:
		# parse record
		splitR = record.split('-')
		module = splitR[0]
		port = splitR[1]

		# build up dict
		if module in moduleToPorts:
			moduleToPorts[module].add(port)
		else:
			moduleToPorts[module] = set([port])
	
	return moduleToPorts




def main():

	# parse command line options
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " cogent_master_atlas"
		sys.exit(1)
	
	# read file
	with open(sys.argv[1], 'r') as masterAtlas:
		# get list of routers
		routers, totalCount, skipCount = getRouters(masterAtlas)
		
		# calculate number of modules and ports per router
		modulesAndPorts = {}
		for routerName, moduleStrings in routers.items():
			modulesAndPorts[routerName] = getModules(moduleStrings)

		# calculate  number of modules on each router
		moduleCounts = {}
		for routerName, moduleToPorts in modulesAndPorts.items():
			moduleCounts[routerName] = len(moduleToPorts.keys())

		# calculate number of ports on each module
		portCounts = {}
		numPortsPerModule = []
		for routerName, moduleToPorts in modulesAndPorts.items():
			numPorts = map(len, moduleToPorts.values())
			portCounts[routerName] = sum(numPorts)
			numPortsPerModule.extend(numPorts)

		# calculate avg module count in all routers
		avgModules = sum(moduleCounts.values())/(1.0 * len(modulesAndPorts)) # total number of modules / number of routers

		# calculate avg port density in all routers
		avgPortDensity = sum(numPortsPerModule)/(1.0 * len(numPortsPerModule)) # average of the port densities for each module

		# calculate max port density
		maxPortDensity = max(numPortsPerModule)

		# find routers with most modules
		routersWithManyModules = sorted(moduleCounts.keys(), key=lambda x: moduleCounts[x], reverse=True)

		# find routers with most ports
		routersWithManyPorts = sorted(modulesAndPorts.keys(), key=lambda x:  sum(map(len, modulesAndPorts[x].values())), reverse=True)
		
		# print statistics
		print "DNS Records Skipped: " + str(skipCount) + " (" + str((100.0 * skipCount / totalCount)) + "% of total)"
		print "Avg Modules/Router: " + str(avgModules) 
		print "Avg Port Density/Module: " + str(avgPortDensity)
		print "Max Port Density/Module: " + str(maxPortDensity)
		print "Routers With Most Modules:"
		for i in range(0,5):
			routerName = routersWithManyModules[i]
			print "\t" + routerName + " : " + str(moduleCounts[routerName])
		print "Routers With Most Ports:"
		for i in range(0,5):
			routerName = routersWithManyPorts[i]
			print "\t" + routerName + " : " + str(portCounts[routerName])



if __name__ == "__main__":
	main()
