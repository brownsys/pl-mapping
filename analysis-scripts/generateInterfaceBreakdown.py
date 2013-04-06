#!/usr/bin/python
"""
Writes the breakdown week-by-week of Cogent's physical interfaces
as reported by DNS records.

Data is output in the following format to be compatible with gnuplot.

# Week	Type			Count
  1	FastEthernet		10
  1	10GigabitEthernet	200
  ...
"""

import os
import sys
import re

# options
valueTabSeparator = "\t"
headerTabSeparator = "\t"
allWeeks = False
physicalOnly = False
virtualOnly = False
normalized = False

def getInterfaceType(intr_abbr):
	abbreviations = {
		# Physical Interfaces
		'FastEthernet': "Physical",
		'GigabitEthernet': "Physical",
		'TenGigabitEthernet': "Physical",
		'Ethernet': "Physical",
		'Fddi': "Physical",
		'ATM': "Physical",
		'POS': "Physical",
		'Serial': "Physical",
		'Serial': "Physical",
		'IntegratedServicesModule': "Physical",
		'Pos-channel': "Physical",

		# Virtual Interfaces
		'Vlan': "Virtual",
		'Multilink': "Virtual",
		'Tunnel': "Virtual",
		'Loopback': "Virtual",
		'Virtual-Access': "Virtual",
		'Virtual-Template': "Virtual",

		# Unknown Interfaces
		'EOBC': "Unknown",
		'Async': "Unknown",
		'Group-Async': "Unknown",
		'MFR': "Unknown"
	}

	try:
		return abbreviations[intr_abbr]
	except KeyError:
		return "Unknown"

"""
Takes in a COGENT-MASTER-ATLAS.txt file for a week and
reads it to get the interface breakdown. Returns three
dictionaries one with physical interfaces -> count,
another for virtual interfaces -> count, and another
for unknown interfaces -> count.
"""
def getBreakdown(masterAtlas):
	physicalInterfaces = {}
	virtualInterfaces = {}
	unknownInterfaces = {}

	# iterate through entries in file
	for line in masterAtlas.readlines():
		# split line into usuable chunks
		splitLine = re.split("\s+", line.strip());
		if len(splitLine) != 6: 
			continue

		# only interested in first two chars
		interfaceString = splitLine[5]
		interfaceType = getInterfaceType(interfaceString)

		# increment dictionary counts
		if interfaceType == "Physical":
			if interfaceString in physicalInterfaces:
				physicalInterfaces[interfaceString] += 1
			else:
				physicalInterfaces[interfaceString] = 1
		elif interfaceType == "Virtual":
			if interfaceString in virtualInterfaces:
				virtualInterfaces[interfaceString] += 1
			else:
				virtualInterfaces[interfaceString] = 1
		else:
			if interfaceString in unknownInterfaces:
				unknownInterfaces[interfaceString] += 1
			else:
				unknownInterfaces[interfaceString] = 1
	
	return physicalInterfaces, virtualInterfaces, unknownInterfaces

"""
Nicely print an int or float
"""
def trunc(f):
	if isinstance(f, int):
		return str(f)
	slen = len('%.*f' % (2,f))
	return str(f)[:slen]

"""
Prints GNUPlot friendly version of a list of dictionaries
"""
def printGNUPlotData(alist, firstColumnKey):
	if len(alist) == 0:
		return

	firstdict = alist[0]
	if len(firstdict.keys()) == 0:
		return
	if firstColumnKey == None:
		firstColumnKey =  firstdict.keys()[0]
	
	# print header
	header = "# "
	header += (str(firstColumnKey) + headerTabSeparator)
	for column in firstdict.keys():
		if column != firstColumnKey:
			header += (str(column) + headerTabSeparator)
	header.strip(headerTabSeparator)
	print header

	# print data
	for adict in alist:
		row = ""
		row += (trunc(adict[firstColumnKey]) + valueTabSeparator)
		for column in adict:
			if column != firstColumnKey:
				row += (trunc(adict[column]) + valueTabSeparator)
		row.strip(valueTabSeparator)
		print row

"""
Analyze one COGENT-MASTER-ATLAS.txt file and returns the analysis in a dictionary.
"""
def analyzeOneFile(masterAtlas):			
	# get breakdown
	physicalInterfaces, virtualInterfaces, unknownInterfaces = getBreakdown(masterAtlas)

	# extract relevant information
	selectedDict = {}
	if physicalOnly:
		selectedDict = physicalInterfaces
	elif virtualOnly:
		selectedDict = virtualInterfaces
	else:
		selectedDict = {"Physical" : sum(physicalInterfaces.values()), "Virtual" : sum(virtualInterfaces.values()) }

	# normalize if necessary
	if normalized:
		selectedDictSum = float(sum(selectedDict.values()))
		for item in selectedDict:
			selectedDict[item] = float(selectedDict[item]/selectedDictSum)
	return selectedDict

def main():

	global allWeeks
	global physicalOnly
	global virtualOnly
	global normalized

	# parse command line options
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + "file [options]"
		print "Options:"
		print "\t--allWeeks\tInterpret \"file\" argument as directory containing subdirectories of weeks with files"
		print "\t--physical\tGet breakdown of physical interfaces"
		print "\t--virtual\tGet breakdown of virtual interfaces"
		print "\t--normalized\tNormalize results"
		print "\tNOTE: When neither the physical or virtual flags are present, the ratio of physical to virtual are reported"
		sys.exit(1)

	options = set(sys.argv[2:])
	if "--allWeeks" in options:
		allWeeks = True
	if "--physical" in options:
		physicalOnly = True
	if "--virtual" in options:
		virtualOnly = True
	if "--normalized" in options:
		normalized = True

	# analyze a single file or all the files
	if allWeeks:
		try:
			pl_archives = sys.argv[1]
			selectedDictList = []
			for weekdir in os.listdir(pl_archives):
				try:
					masterAtlas = open(pl_archives + "/" + weekdir + "/" + "COGENT-MASTER-ATLAS.txt", "r")
					selectedDict = analyzeOneFile(masterAtlas)
					selectedDict["Week"] = int(weekdir)
					selectedDictList.append(selectedDict)
					masterAtlas.close()
				except:
					raise
					sys.stderr.write("Skipping directory " + weekdir + "\n")
			selectedDictList = sorted(selectedDictList, key=lambda x:x["Week"])
			printGNUPlotData(selectedDictList, "Week")
		except:
			raise
			sys.stderr.write("Could not open directory " + dirname + "\n")
			sys.exit(1)
	else:
		try:
			filename = sys.argv[1]
			masterAtlas = open(filename, "r")
			selectedDict = analyzeOneFile(masterAtlas)
			masterAtlas.close()
			printGNUPlotData([selectedDict], None)
		except:
			sys.stderr.write("Could not open file " + filename + "\n")
			sys.exit(1)

if __name__ == "__main__":
	main()
