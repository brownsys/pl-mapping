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

stdoutFormat = \
"# Named routers as determined by iffinder and reverse DNS records
# Name\tIPs
%s
# Iffinder/DNS Disagreements
# DNS Name\tiffinder Name\tIPs
%s
# IPs with multiple reverse reverse DNS records
# Name\tIPs
%s"

"""
Takes in a iffinder-analysis stdout and stderr dump for a week and
reads it to get interesting informating.
"""
def getIffinderInfo(stdoutFile, stderrFile):
	# extract data from file
	stderrContent = stderrFile.read()
	stderrData = scanf.sscanf(stderrContent, stderrFormat)
	stdoutContent = stdoutFile.read()
	stdoutData = scanf.sscanf(stdoutContent, stdoutFormat)

	print stderrData
	print stdoutData

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
Analyze one week's files and returns the analysis in a dictionary.
"""
def analyzeOneFile(weekNumber):			
	# open the week's file for reading
	stdoutFilename = weekNumber + ".stdout.txt"
	stdoutFile = open(stdoutFilename, "r")
	stderrFilename = weekNumber + ".stderr.txt"
	stderrFile = open(stderrFilename, "r")
	
	getIffinderInfo(stdoutFile, stderrFile)


def main():
	global allWeeks
	global numRouters
	global averageDegree
	global disagreement

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
			iffinder_analysis = sys.argv[1]
			for weekfiles in os.listdir(iffinder_analysis):
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

if __name__ == "__main__":
	main()
