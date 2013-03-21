#!/usr/bin/python

import sys

ipIndex = {}

# Creates a dictionary from IP address (in decimal) to
#     {ip addr, interface type, location, router in that location}
for line in sys.stdin.readlines():
    pieces = line.split()
    model = pieces[-1]
    ip_txt = pieces[-2]
    loc    = pieces[0]
    router = pieces[1]

    ip_parts = ip_txt.split(".")
    ip = int(ip_parts[0]) * 256 * 256 * 256 + \
            int(ip_parts[1]) * 256 * 256 + int(ip_parts[2]) * 256 + \
            int(ip_parts[3])

    ipIndex[ip] = (ip_txt, model, loc, router)

# Hunts for /30's where we have both usable IPs in our list of routers
last_val = -1
for val in sorted(ipIndex):
    if (val - last_val) == 1 and \
            ((val + 1) not in ipIndex) and \
            ((val - 2) not in ipIndex) and \
            ((val - 2) % 4 == 0):
        print("%s\t%s\t%s\t%s\t" % ipIndex[last_val]),
        print("%s\t%s\t%s\t%s" % ipIndex[val])
    last_val = val
