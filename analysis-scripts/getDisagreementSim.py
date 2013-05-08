#!/usr/bin/python

import sys
import os
import re

"""
Takes in an opened iffinder analysis stdout file.
Returns a set of the strings found in the disagreements section.
"""
def getDisagreements(iffinderFile):

	disagreements = set()

	# loop over stdout file
	hashSymbolCounter = 0
	for line in iffinderFile.readlines():
		# count comments to get to disagreements section
		if line[0] == '#':
			# when we see our fifth comment we've reached the
			# end of the disagreements section
			if hashSymbolCounter == 4:
				break
			else:
				hashSymbolCounter += 1
				continue
		else:
			# skip all lines before disagreement section
			if hashSymbolCounter < 4:
				continue
			disagreements.add(line.strip())
	
	return disagreements

"""
Returns a string version of set of strings
"""
def setToString(aset):
	result = ""
	for item in aset:
		result += "(" + item.replace("\t", ", ") + "), "
	return result.strip(", ")


def main():

	# parse command line options
	if len(sys.argv) != 2:
		print "Usage: " + sys.argv[0] + " iffinder_analysis"
		sys.exit(1)
	try:
		iffinder_analysis = sys.argv[1]

		# get weeks available in directory
		weeks = set()
		for weekfile in os.listdir(iffinder_analysis):
			weekNumber= weekfile.split(".")
			if weekNumber[0].isdigit():
				weeks.add(int(weekNumber[0]))
		weeks = sorted(weeks)

		# open week files
		disagreementTracker = {} # disagreement to number of continuous weeks it appears
		inDisagreement = set() # set of persistent disagreements
		finalDisagreements = {} # disagreement to list of number of continusous weeks it appears
		for week in weeks:
			try:
				# open relevant file
				currWeekFilename = iffinder_analysis + "/" + str(week) + ".stdout.txt"
				currWeekFile = open(currWeekFilename, "r")

				# get sets of DNS/iffinder disagreements
				currWeekDisagreements = getDisagreements(currWeekFile)
				
				# update disagreementTracker
				for disagreement in currWeekDisagreements:
					if disagreement not in disagreementTracker:
						disagreementTracker[disagreement] = 1
					else:
						if disagreement in inDisagreement:
							disagreementTracker[disagreement] += 1
						else:
							# this branch represents the unexpected case
							# where a disagreement reappears in the data
							# after not being in disagreement for at least
							# one week. We hack here.
							if disagreement in finalDisagreements:
								finalDisagreements[disagreement].append(disagreementTracker[disagreement])
							else:
								finalDisagreements[disagreement] = [disagreementTracker[disagreement]]
							disagreementTracker[disagreement] = 1

				# update inDisagreement
				inDisagreement = currWeekDisagreements
			except:
				raise
		
		# merge dictionaries
		for disagreement, count in disagreementTracker.items():
			if disagreement in finalDisagreements:
				finalDisagreements[disagreement].append(count)
			else:
				finalDisagreements[disagreement] = [count]
			
		# generate histogram
		weeksToCount = {}
		weeksToDisagreements = {} # for finding outliers
		for disagreement, listOfWeeks in finalDisagreements.items():
			for numWeeks in listOfWeeks:
				if numWeeks in weeksToCount:
					weeksToCount[numWeeks] += 1
				else:
					weeksToCount[numWeeks] = 1
				if numWeeks in weeksToDisagreements:
					weeksToDisagreements[numWeeks].add(disagreement)
				else:
					weeksToDisagreements[numWeeks] = set([disagreement])

		# print main results
		print "# WeeksOfDisagreement\tCount"
		for numWeeks in sorted(weeksToCount.keys()):
			print str(numWeeks) + "\t" + str(weeksToCount[numWeeks])

		# print outliers
		outliers = sorted(weeksToDisagreements.keys(), reverse=True)[:5]
		for outlier in outliers:
			sys.stderr.write(setToString(weeksToDisagreements[outlier]) + " : " + str(outlier) + "\n")

	except:
		raise
		sys.stderr.write("Error: Could not open iffinder_analysis.\n")
		sys.exit(1)



if __name__ == "__main__":
	main()
