#!/usr/bin/python

import sys

ipIndex = {}

for line in sys.stdin.readlines():
	pieces = line.split()
	model = pieces[-1]
	ip_txt = pieces[-2]
	loc	= pieces[0]
	router = pieces[1]

	ip_parts = ip_txt.split(".")
	ip = int(ip_parts[0]) * 256 * 256 * 256 + \
			int(ip_parts[1]) * 256 * 256 + int(ip_parts[2]) * 256 + \
			int(ip_parts[3])

	ipIndex[ip] = (ip_txt, model, loc, router)

last_val = -1
for val in sorted(ipIndex):
	if (val - last_val) == 1:
		print("%s\t%s\t%s\t%s\t" % ipIndex[last_val]),
		print("%s\t%s\t%s\t%s" % ipIndex[val])
#		print "%s %s" % (ipIndex[last_val], ipIndex[val])
	last_val = val
