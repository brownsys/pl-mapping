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
		'fa': ('FastEthernet', "Physical"),
		'gi': ('GigabitEthernet', "Physical"),
		'te': ('TenGigabitEthernet', "Physical"),
		'et': ('Ethernet', "Physical"),
		'fd': ('Fddi', "Physical"),
		'mu': ('Multilink', "Physical"),
		'at': ('ATM', "Physical"),
		'po': ('POS', "Physical"),
		'se': ('Serial', "Physical"),
		'Se': ('Serial', "Physical"),

		# Virtual Interfaces
		'vl': ('Vlan', "Virtual"),
		'is': ('IntegratedServicesModule', "Virtual"),
		'tu': ('Tunnel', "Virtual"),
		'lo': ('Loopback', "Virtual"),
		'vi': ('Virtual-Access', "Virtual"),
		'vt': ('Virtual-Template', "Virtual"),

		# Unknown Interfaces
		'eo' : ('EOBC', "Unknown"),
		'posch': ('Pos-channel', "Unknown"),
		'async': ('Async', "Unknown"),
		'group-async': ('Group-Async', "Unknown"),
		'mfr': ('MFR', "Unknown")
	}

	try:
		return abbreviations[intr_abbr]
	except KeyError:
		return ("(unknown)", "Unknown")

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
		interfaceString, interfaceType = getInterfaceType(splitLine[2][:2])

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
def printGNUPlotData(alist):
	if len(alist) == 0:
		return
	
	# print header
	firstdict = alist[0]
	header = "# "
	for column in firstdict.keys():
		header += (str(column) + headerTabSeparator)
	header.strip(headerTabSeparator)
	print header

	# print data
	for adict in alist:
		row = ""
		for column in adict:
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


"""
               _       _         _             _         _                   
 ___  ___ _ __(_)_ __ | |_   ___| |_ __ _ _ __| |_ ___  | |__   ___ _ __ ___ 
/ __|/ __| '__| | '_ \| __| / __| __/ _` | '__| __/ __| | '_ \ / _ \ '__/ _ \
\__ \ (__| |  | | |_) | |_  \__ \ || (_| | |  | |_\__ \ | | | |  __/ | |  __/
|___/\___|_|  |_| .__/ \__| |___/\__\__,_|_|   \__|___/ |_| |_|\___|_|  \___|
                |_|                                                          
"""
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
		printGNUPlotData(selectedDictList)
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
		printGNUPlotData([selectedDict])
	except:
		sys.stderr.write("Could not open file " + filename + "\n")
		sys.exit(1)
