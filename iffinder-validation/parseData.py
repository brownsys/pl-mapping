#!/usr/bin/python
"""
Reads iffinder content and parse it into tuples structured as follows:

	(addr, alias, o-TTL-r, RTT, result)

Then, these tuples are checked for similarity and lists of addrs are
calculated such that each list contains IPs which are believed to belong
to interfaces on the same router.
"""
import sys
import re

# statistics
numParsed = 0
numUniqueAlias = 0
avgInterfaces = 0

# parse the file into usable tuples
parsed = []
for line in sys.stdin.readlines():
	# check if line is a comment
	if line[0] == "#":
		continue

	# try and parse line
	splitLine = re.split("\s+", line.strip())
	if len(splitLine) == 8:
		addr = splitLine[0]
		alias = splitLine[1]
		oTTLr = (splitLine[2], splitLine[3])
		RTT = splitLine[4]
		iffResult = splitLine[5]
		theTuple = (addr, alias, oTTLr, RTT, iffResult)
		parsed.append(theTuple)
	else:
		continue

# build a dictionary of alias IPs { alias IP -> [ interface IPs ] }
aliases = {}

# load candidates based on aliases responses
for entry in parsed:
	addr = entry[0]
	alias = entry[1]
	if alias in aliases:
		aliases[alias].append(addr)
	else:
		aliases[alias] = [addr]

#TODO: Compensate for "results" field

#TODO: What additional sanity checks do we need?
#	-Crunch data in graphs to reduce aliasing data
#	-Reverse DNS record similarities

#TODO: Graph edge analysis?
#	-/30 blocks should be connected by a link
#	-Traceroute shows connections



numParsed = len(parsed)
numUniqueAlias = len(aliases.keys())
lengthsOfAliases = map(len, aliases.values())
avgInterfaces = sum(lengthsOfAliases)/len(aliases.keys())

sys.stderr.write("Number of lines parsed: " + str(numParsed) + "\n")
sys.stderr.write("Number of unique aliases found: " + str(numUniqueAlias) + " (" + str(int((numUniqueAlias / (1.0 * numParsed)) * 100)) +"% of parsed)\n")
sys.stderr.write("Number of addrs to aliases:\n\tAvg: " + str(avgInterfaces) + "\n\tMax: " + str(max(lengthsOfAliases)) + "\n\tMin: " + str(min(lengthsOfAliases)) + "\n")
