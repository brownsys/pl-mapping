#!/usr/bin/python
"""
Writes the breakdown week-by-week of Cogent's router breakdown
as reported by DNS records and iffinder

Data is output in the following format to be compatible with gnuplot.

# Week	Average Degree
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
allWeeks = False
numRouters = False
averageDegree = False
disagreement = False


stderrFormat = \
"-----------------
iffinder results:
	Number of routers found: %d
	Number of non-responsive IPs: %d
	Number of discovered IPs: %d
	Number of addrs to aliases:
		Avg: %f
		Avg more-than one: %f
		Max: %d
		Min: %d
dns record results:
	Number of names found: %d
	Number of ips with multiple reverse DNS records: %d
	Number of IPs to names:
		Avg: &f
		Avg more-than one: %f
		Max: %d
		Min: %d
Non-unanimous agreement in iffinder and dns record analysis: %d (%d%% of total)
-----------------"

"""
Takes in a iffinder-analysis stderr dump for a week and
reads it to get interesting informating.
"""
def getIffinderInfo(stderrFile):
	# extract data from file
	stderrContent = stderrFile.read()
	data = scanf.sscanf(stderrContent, stderrFormat)

	# reduce to relevant data
	relevant = []




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
	print "\t--allWeeks\tInterpret \"file\" argument as directory containing iffinder-analysis files"
	print "\t--num-routers\tGet number of routers"
	print "\t--average-degree\tGet ratio of interface/routers"
	print "\t--disagreement\tGet number of disagreements between DNS and iffinder"
	sys.exit(1)

options = set(sys.argv[2:])
if "--allWeeks" in options:
	allWeeks = True
if "--num-routers" in options:
	numRouters = True
if "--average-degree" in options:
	averageDegree = True
if "--disagreement" in options:
	disagreement = True

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
