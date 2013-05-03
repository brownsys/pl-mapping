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
from routerInterfaces import getBreakdown

# options
valueTabSeparator = "\t"
headerTabSeparator = "\t"


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
a tuple containing sets of physical, virtual, and all IPs for that week.
Returns a list of the number of physical IPs on each router.
"""
def getDegrees(stdoutFile, interfaceBreakdown):
	# get interface sets
	physicalInterfaces = interfaceBreakdown[0]
	virtualInterfaces = interfaceBreakdown[1]

	# extract data from stdout file
	commentCounter = 0
	physIPListLengths = []
	virtIPListLengths = []
	for line in stdoutFile.readlines():
		# look for commment lines
		if commentCounter > 2:
			break
		if line[0] == "#":
			commentCounter += 1
			continue
		# read router info
		splitLine = line.split("\t")
		physIPs = []
		virtIPs = []
		for ip in getList(splitLine[1]):
			if ip in physicalInterfaces:
				physIPs.append(ip)
			elif ip in virtualInterfaces:
				virtIPs.append(ip)
		physListLen = len(physIPs)
		virtListLen = len(virtIPs)
		if physListLen > 0:
			physIPListLengths.append(physListLen)
		if virtListLen > 0:
			virtIPListLengths.append(virtListLen)

	return physIPListLengths


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
			weekNumber = re.findall(r'\d+', filename)[0]
			masterAtlas = open(pl_archives + "/" + weekNumber + "/" + "COGENT-MASTER-ATLAS-FIXED.txt", "r")
			interfaceBreakdown = getBreakdown(masterAtlas)
			masterAtlas.close()

			# process single file without binning
			stdoutFile = open(filename, "r")
			listOfDegrees = getDegrees(stdoutFile, interfaceBreakdown)
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
			#selectedDictList = []
			print "# Degree\tWeek"
			for week in weeks:
				try:
					# open stdout dump file
					stdoutFilename = filename + "/" + week + ".stdout.txt"
					stdoutFile = open(stdoutFilename, "r")
					
					# get physical interface IPs
					masterAtlas = open(pl_archives + "/" + week + "/" + "COGENT-MASTER-ATLAS-FIXED.txt", "r")
					interfaceBreakdown = getBreakdown(masterAtlas)
					masterAtlas.close()

					# get degree information from file
					listOfDegrees = getDegrees(stdoutFile, interfaceBreakdown)
					#histogramDict = generateHistogram(listOfDegrees)

					# print columns of data
					for degree in listOfDegrees:
						print degree + "\t" + week

					# bin the information from file
					#selectedDict = createBinDict(int(week))
					#for key, value in histogramDict.items():
					#	binTag = getBin(key)
					#	selectedDict[binTag] += value
					#selectedDictList.append(selectedDict)

				except:
					raise
					sys.stderr.write("Skipping week " + week + "\n")

			# print GNUPlot compatible data
			#selectedDictList = sorted(selectedDictList, key=lambda x:x["Week"])
			#columnKeyList = ["Week"]
			#columnKeyList.extend([item[0] for item in bins])
			#printGNUPlotData(selectedDictList, columnKeyList)
	except:
		raise
		sys.stderr.write("Could not open file/directory " +	iffinder_analysis + "\n")
		sys.exit(1)

if __name__ == "__main__":
	main()
