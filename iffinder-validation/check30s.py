#!/usr/bin/python
"""
Polls Cogent's website to check whether IPs are on the same subnet.
"""

import sys
import requests # to install this, use "easy_install --user requests"
import time


def main():
	if len(sys.argv) != 4:
		print "Usage: " + sys.argv[0] + " pairs_file ipblock_output raw_output"
		sys.exit(1)
	
	# load pairs file
	ipsToLookup = [] # list of IPs to lookup on Cogent's site
	with open(sys.argv[1], 'r') as pairsFile:
		for line in pairsFile.readlines():
			ipsToLookup.append(line.strip().split()[0])

	# open output files
	ipblockFile = open(sys.argv[2], 'w+')
	rawFile = open(sys.argv[3], 'w+')
	
	for ip in ipsToLookup:
		# construct web request
		payload = {"FKT" : "go!", "CMD" : "BGP", "LOC" : "iad03", "DST" : ip}
		headers = {"Content-Type" : "application/x-www-form-urlencoded"}
		r = requests.post("http://www.cogentco.com/lookingglass.php", data=payload, headers=headers)
		if r.status_code != requests.codes.ok:
			sys.stderr.write("Error code " + str(r.status_code) + " unexpectedly returnd for " + ip  + "\n")
			time.sleep(2)
			continue

		# parse request
		preTag = r.text.find("<pre>") + 5
		closeTag= r.text.find("</pre>")
		relevantString = r.text[preTag:closeTag].replace('\r', '\n')
		relevantLines = relevantString.split("\n") # contains the raw response

		# get information to print out
		startOfBlock = len("BGP routing table entry for ")
		endOfBlock = relevantLines[0].find(",")
		block = relevantLines[0][startOfBlock:endOfBlock].strip(" ")
		thirdLine = relevantLines[2]
		blockLine =  ip + "\t" + block + "\t" + thirdLine

		# write to correct files
		print blockLine
		ipblockFile.write(blockLine + "\n")
		rawFile.write("Query: " + ip + "\n" + relevantString + "\n")

		# sleep to not annoy cogent
		time.sleep(1)
	
	sys.stderr.write("DONE")

	ipblockFile.close()
	rawFile.close()



if __name__ == "__main__":
	main()
