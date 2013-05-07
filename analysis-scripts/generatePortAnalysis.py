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

	return routerToDNS.values(), totalCount, skipCount


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
		modulesAndPorts = [getModules(router) for router in routers]

		# calculate statistics
		moduleCounts = map(lambda x: len(x.keys()), modulesAndPorts)
		avgModules = sum(moduleCounts)/(1.0 * len(modulesAndPorts)) # total number of modules / number of routers
		maxModules = max(moduleCounts) # largest number of modules in one router
		avgPortDensities = [sum(map(len, router.values()))/(1.0 * len(router.keys())) for router in modulesAndPorts]
		avgPortDensity = sum(avgPortDensities)/(1.0 * len(avgPortDensities)) # average of the port densities for each module
		maxPorts = max([max(map(len, router.values())) for router in modulesAndPorts])
		
		# print statistics
		print "DNS Records Skipped: " + str(skipCount) + " (" + str((100.0 * skipCount / totalCount)) + "% of total)"
		print "Avg Modules/Router: " + str(avgModules) 
		print "Max Modules/Router: " + str(maxModules)
		print "Avg Port Density/Module: " + str(avgPortDensity)
		print "Max Ports/Module: " + str(maxPorts)



if __name__ == "__main__":
	main()
