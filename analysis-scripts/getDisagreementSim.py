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
			weeks.add(int(weekNumber[0]))
		weeks = sorted(weeks)[1:-1] # sort and chop off ends

		# open week files
		print "# PrevWeek\tCurrWeek\tDiffCount\tPercentDiff"
		for week in weeks:
			try:
				# open relevant files
				prevWeekFilename = iffinder_analysis + "/" + str(week) + ".stdout.txt"
				prevWeekFile = open(prevWeekFilename, "r")
				currWeekFilename = iffinder_analysis + "/" + str(week - 1) + ".stdout.txt"
				currWeekFile = open(currWeekFilename, "r")

				# get sets of DNS/iffinder disagreements
				prevWeekDisagreements = getDisagreements(prevWeekFile)
				currWeekDisagreements = getDisagreements(currWeekFile)
				
				# get similarity between disagreement sets
				disagreementSimilarity = prevWeekDisagreements & currWeekDisagreements
				numSame = len(disagreementSimilarity)
				print str(week-1) + "\t" + str(week) + "\t" + str(numSame) + "\t" + str((100.0 * numSame)/len(currWeekDisagreements))
			except:
				raise

	except:
		raise
		sys.stderr.write("Error: Could not open iffinder_analysis.\n")
		sys.exit(1)



if __name__ == "__main__":
	main()
