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

import sys
import re

def getInterfaceType(intr_abbr):
	abbreviations = {
		# Physical Interfaces
		'fa': ('FastEthernet', "Physical")
		'gi': ('GigabitEthernet', "Physical")
		'te': ('TenGigabitEthernet', "Physical")
		'et': ('Ethernet', "Physical")
		'fd': ('Fddi', "Physical")
		'mu': ('Multilink', "Physical")
		'at': ('ATM', "Physical")

		# Virtual Interfaces
		'vl': ('Vlan', "Virtual")
		'is': ('IntegratedServicesModule', "Virtual")
		'tu': ('Tunnel', "Virtual")
		'lo': ('Loopback', "Virtual")
		'vi': ('Virtual-Access', "Virtual")
		'vt': ('Virtual-Template', "Virtual")

		# Unknown Interfaces
		'eo' : ('EOBC', "Unknown")
		'se': ('Serial', "Unknown")
		'Se': ('Serial', "Unknown")
		'po': ('POS', "Unknown")
		'posch': ('Pos-channel', "Unknown")
		'async': ('Async', "Unknown")
		'group-async': ('Group-Async', "Unknown")
		'mfr': ('MFR'. "Unknown")
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
		splitLine = re.split("\s+", line.strip);
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
               _       _         _             _         _                   
 ___  ___ _ __(_)_ __ | |_   ___| |_ __ _ _ __| |_ ___  | |__   ___ _ __ ___ 
/ __|/ __| '__| | '_ \| __| / __| __/ _` | '__| __/ __| | '_ \ / _ \ '__/ _ \
\__ \ (__| |  | | |_) | |_  \__ \ || (_| | |  | |_\__ \ | | | |  __/ | |  __/
|___/\___|_|  |_| .__/ \__| |___/\__\__,_|_|   \__|___/ |_| |_|\___|_|  \___|
                |_|                                                          
"""
# parse command line options
if len(sys.argv) != 2:
	print "Usage: " + sys.argv[0] + " pl_archives"
	sys.exit(1)

# try and open an COGENT-MASTER-ATLAS.txt file
try:
	fileName = sys.argv[1]
	masterAtlas = sys.open(fileName, "r")
except:
	sys.stderr.write("Could not open file " + fileName + "\n")
	sys.exit(1)

# get breakdown
physicalInterfaces, virtualInterfaces, unknownInterfaces = getBreakdown(masterAtlas)

print physicalInterfaces
