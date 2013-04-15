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


"""
Takes in the printed version of a python list
and returns the list
"""
def getList(string):
	return [item.strip().strip("'") for item in string.lstrip("[").rstrip("]\n").split(",")]

"""
Takes in a iffinder-analysis stdout dump for a week and
returns a list of the number of IPs on each router.
"""
def getDegrees(stdoutFile):
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
		ipListLengths.append(len(getList(splitLine[1])))

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

	# parse command line options
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " iffinder_analysis"
		sys.exit(1)

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
				
				selectedDict = { "Week" : int(week) }
				listOfDegrees = getDegrees(stdoutFile)
				print sorted(listOfDegrees)
				selectedDictList.append(selectedDict)
			except:
				sys.stderr.write("Skipping week " + week + "\n")
		#selectedDictList = sorted(selectedDictList, key=lambda x:x["Week"])
		#printGNUPlotData(selectedDictList, "Week")
	except:
		sys.stderr.write("Could not open directory " +	iffinder_analysis + "\n")
		sys.exit(1)

if __name__ == "__main__":
	main()
