#!/usr/bin/python
"""
Creates a week-by-week histogram of Cogent's router degree
as reported by DNS records and iffinder

Data is output in the following format to be compatible with gnuplot.

# Week	1-10 10-20 20-30...
  1	256		
  11	200		
  ...
"""

# sscanf like module borrowed from dyoo
# https://hkn.eecs.berkeley.edu/~dyoo/python/scanf/scanf-1.2.tar.gz
import scanf
import os
import sys
import re

# options
valueTabSeparator = "\t"
headerTabSeparator = "\t"

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
Takes in a COGENT-MASTER-ATLAS-FIXED.txt file for a week and
reads it to get the interface breakdown. Returns three
set of IPs, physical interfaces, virtual interfaces and unknown,
"""
def getBreakdown(masterAtlas):
	physicalInterfaces = set()
	virtualInterfaces = set()
	unknownInterfaces = set()

	# iterate through entries in file
	for line in masterAtlas.readlines():
		# split line into usuable chunks
		splitLine = re.split("\s+", line.strip());
		if len(splitLine) != 6: 
			continue

		# only interested in first two chars
		ip = splitLine[4]
		interfaceString = splitLine[5]
		interfaceType = getInterfaceType(interfaceString)

		# build up sets
		if interfaceType == "Physical":
			physicalInterfaces.add(ip)
		elif interfaceType == "Virtual":
			virtualInterfaces.add(ip)
		else:
			unknownInterfaces.add(ip)
	
	return physicalInterfaces, virtualInterfaces, unknownInterfaces


"""
Set of bins as defined by a tuple

("Bin TAG", lambda to classify items in this bin)

"""
bins = 	[("<5", lambda x: x < 5), \
	("5-10", lambda x: x >= 5 and x < 10), \
	("10-20", lambda x: x >= 10 and x < 20), \
	("20-100", lambda x: x >= 20 and x < 100), \
	("100-300", lambda x: x >= 100 and x < 300), \
	(">300", lambda x: x >= 300)]


"""
Loop through the lists defined above for binning and print the
bin a key belongs in
"""
def getBin(key):
	for abin in bins:
		if abin[1](int(key)):
			return abin[0]

	# SHOULD NEVER GET HERE
	sys.exit("couldn't bin key " + str(key))


"""
Create a dict to be printed for gnuPlotting. Initializes all bin
entries to 0.
"""
def createBinDict(week):
	newDict = { "Week" : week }
	for tag in bins:
		newDict[tag[0]] = 0
	return newDict


"""
Takes a list of values and produces a dictionary verison of a histogram
"""
def generateHistogram(alist):
	histogram = {}
	for item in alist:
		stritem = str(item)
		if stritem in histogram:
			histogram[stritem] += 1
		else:
			histogram[stritem] = 1
	return histogram


"""
Takes in the printed version of a python list
and returns the list
"""
def getList(string):
	return [item.strip().strip("'") for item in string.lstrip("[").rstrip("]\n").split(",")]


"""
Takes in a iffinder-analysis stdout dump for a week and
a set of physical interface IPs for that week.
Returns a list of the number of physical IPs on each router.
"""
def getDegrees(stdoutFile, physicalInterfaces):
	# extract data from stdout file
	commentCounter = 0
	ipListLengths = []
	for line in stdoutFile.readlines():
		# look for commment lines
		if commentCounter > 2:
			break
		if line[0] == "#":
			commentCounter += 1
			continue
		# read router info
		splitLine = line.split("\t")
		ipListLengths.append(len(filter(lambda x: x in physicalInterfaces, getList(splitLine[1]))))

	return ipListLengths


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
def printGNUPlotData(alist, columnKeyList):
	# can't print an empty list
	if len(alist) == 0:
		return

	# get first dict, can't print list of empty dicts
	firstdict = alist[0]
	if len(firstdict.keys()) == 0:
		return

	# set default values for non-set options
	if columnKeyList == None:
		columnKeyList = firstdict.keys()
	
	# print header
	header = "# "
	for column in columnKeyList:
		header += (str(column) + headerTabSeparator)
	header.strip(headerTabSeparator)
	print header

	# print data
	for adict in alist:
		row = ""
		for column in columnKeyList:
			row += (trunc(adict[column]) + valueTabSeparator)
		row.strip(valueTabSeparator)
		print row


def main():

	# parse command line options
	if len(sys.argv) < 3:
		print "Usage: " + sys.argv[0] + " <stdout dump OR dir containing stdout dumps> <pl_archives>"
		sys.exit(1)

	# perform analysis
	try:
		# process stdout dump
		filename = sys.argv[1]	
		pl_archives = sys.argv[2]
		if os.path.isfile(filename):
			# get physical interface IPs
			weekNumber= filename.split(".")[0]
			masterAtlas = open(pl_archives + "/" + weekNumber + "/" + "COGENT-MASTER-ATLAS-FIXED.txt", "r")
			physicalInterfaces, virtualInterfaces, unknownInterfaces = getBreakdown(masterAtlas)
			masterAtlas.close()

			# process single file without binning
			stdoutFile = open(filename, "r")
			listOfDegrees = getDegrees(stdoutFile, physicalInterfaces)
			histogramDict = generateHistogram(listOfDegrees)

			# make printable for GNUPlot
			selectedDictList = []
			for key, value in histogramDict.items():
				selectedDictList.append({ "Degree" : int(key), "Count" : value })	
			selectedDictList = sorted(selectedDictList, key=lambda x:x["Degree"])
			printGNUPlotData(selectedDictList, ["Degree", "Count"])

		else:
			# get weeks available in directory
			weeks = set()
			for weekfile in os.listdir(filename):
				weekNumber= weekfile.split(".")
				weeks.add(weekNumber[0])

			# open week files
			selectedDictList = []
			for week in weeks:
				try:
					# open stdout dump file
					stdoutFilename = filename + "/" + week + ".stdout.txt"
					stdoutFile = open(stdoutFilename, "r")
					
					# get physical interface IPs
					masterAtlas = open(pl_archives + "/" + week + "/" + "COGENT-MASTER-ATLAS-FIXED.txt", "r")
					physicalInterfaces, virtualInterfaces, unknownInterfaces = getBreakdown(masterAtlas)
					masterAtlas.close()

					# get degree information from file
					listOfDegrees = getDegrees(stdoutFile, physicalInterfaces)
					histogramDict = generateHistogram(listOfDegrees)

					# bin the information from file
					selectedDict = createBinDict(int(week))
					for key, value in histogramDict.items():
						binTag = getBin(key)
						selectedDict[binTag] += value
					selectedDictList.append(selectedDict)

				except:
					raise
					sys.stderr.write("Skipping week " + week + "\n")

			# print GNUPlot compatible data
			selectedDictList = sorted(selectedDictList, key=lambda x:x["Week"])
			columnKeyList = ["Week"]
			columnKeyList.extend([item[0] for item in bins])
			printGNUPlotData(selectedDictList, columnKeyList)
	except:
		raise
		sys.stderr.write("Could not open file/directory " +	iffinder_analysis + "\n")
		sys.exit(1)

if __name__ == "__main__":
	main()
