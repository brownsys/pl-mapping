#!/usr/bin/python
"""
Writes the breakdown week-by-week of Cogent's router breakdown
as reported by DNS records and iffinder

Data is output in the following format to be compatible with gnuplot.

# Week	AverageDegree
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
numRouters = False
averageDegree = False
disagreement = False

stderrFormat = \
"-----------------\n" \
"iffinder results:\n" \
	"\tNumber of routers found: %d\n" \
	"\tNumber of non-responsive IPs: %d\n" \
	"\tNumber of discovered IPs: %d\n" \
	"\tNumber of addrs to aliases:\n" \
		"\t\tAvg: %f\n" \
		"\t\tAvg more-than one: %f\n" \
		"\t\tMax: %d\n" \
		"\t\tMin: %d\n" \
"dns record results:\n" \
	"\tNumber of names found: %d\n" \
	"\tNumber of ips with multiple reverse DNS records: %d\n" \
	"\tNumber of IPs to names:\n" \
		"\t\tAvg: %f\n" \
		"\t\tAvg more-than one: %f\n" \
		"\t\tMax: %d\n" \
		"\t\tMin: %d\n" \
"Non-unanimous agreement in iffinder and dns record analysis: %d (%d%% of total)\n" \
"-----------------"

"""
Takes in the printed version of a python list
and returns the list
"""
def getList(string):
	return [item.strip().strip("'") for item in string.lstrip("[").rstrip("]\n").split(",")]

"""
Takes in a iffinder-analysis stdout and stderr dump for a week and
reads it to get interesting informating.
"""
def getIffinderInfo(stdoutFile, stderrFile):
	# extract data from stderr file
	stderrContent = stderrFile.read()
	stderrData = scanf.sscanf(stderrContent, stderrFormat)

	# extract data from stdout file
	commentCounter = 0
	routerNameToIPs = {}
	for line in stdoutFile.readlines():
		# look for commment lines
		if commentCounter > 2:
			break
		if line[0] == "#":
			commentCounter += 1
			continue
		# read router info
		splitLine = line.split("\t")
		routerNameToIPs[splitLine[0]] = getList(splitLine[1])

	# reduce to relevant data
	disagreements = stderrData[13]

	return disagreements, routerNameToIPs


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

def main():
	global allWeeks
	global numRouters
	global averageDegree
	global disagreement

	# parse command line options
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " iffinder_analysis [options]"
		print "Options:"
		print "\t--num-routers\tGet number of routers"
		print "\t--average-degree\tGet ratio of interface/routers"
		print "\t--disagreement\tGet number of disagreements between DNS and iffinder"
		sys.exit(1)

	# parse options
	options = set(sys.argv[2:])
	if "--num-routers" in options:
		numRouters = True
	if "--average-degree" in options:
		averageDegree = True
	if "--disagreement" in options:
		disagreement = True

	# perform analysis
	try:
		iffinder_analysis = sys.argv[1]

		# get weeks available in directory
		weeks = set()
		for weekfile in os.listdir(iffinder_analysis):
			weekNumber= weekfile.split(".")
			weeks.add(weekNumber[0])

		# open week files
		selectedDictList = []
		for week in weeks:
			try:
				stdoutFilename = iffinder_analysis + "/" + week + ".stdout.txt"
				stdoutFile = open(stdoutFilename, "r")
				stderrFilename = iffinder_analysis + "/" + week + ".stderr.txt"
				stderrFile = open(stderrFilename, "r")
				
				selectedDict = { "Week" : int(week) }
				disagreements, routerNameToIPs = getIffinderInfo(stdoutFile, stderrFile)
				if numRouters:
					selectedDict["RouterCount"] = len(routerNameToIPs)
				if averageDegree:
					selectedDict["AverageDegree"] = float(sum(map(len, routerNameToIPs.values())))/float(len(routerNameToIPs))
				if disagreement:
					selectedDict["DisagreementCount"] = disagreements
				selectedDictList.append(selectedDict)
			except:
				sys.stderr.write("Skipping week " + week + "\n")
		selectedDictList = sorted(selectedDictList, key=lambda x:x["Week"])
		printGNUPlotData(selectedDictList, "Week")
	except:
		sys.stderr.write("Could not open directory " +	iffinder_analysis + "\n")
		sys.exit(1)

if __name__ == "__main__":
	main()
