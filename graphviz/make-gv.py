#!/usr/bin/python

import sys

# Input lines look like:
# 38.19.1.129	FastEthernet	ewr01	oob01	38.19.1.130	FastEthernet	ewr01	ca01

links = set()

# clean out some bogus data
bogus = ["demarc", "Moon_Capital_Investments", "Project-Leadership-Associates",
         "Refco_Group_Ltd_LLC", "Cathay_Financial_LLC", "FEV"]

for line in sys.stdin:
    pieces = line[:-1].split('\t')
    src = pieces[2] # [0:3] ... gives us just the cities
    src_router = pieces[3]
    dst = pieces[6] # [0:3]
    dst_router = pieces[7]
    src_ip = pieces[0]

    if src in bogus:
        continue
    if dst in bogus:
        continue
    # clean out pairs from 38/8. According to Cogent's Looking Glass,
    # they don't seem to be valid /30 pairs, and were introducing bogus
    # links in our dataset
    if src_ip.startswith("38."): 
        continue

    if src != dst:
        links.add(tuple(sorted([src, dst])))


# Do not add edge attributes, This graph will be parsed by the Gephi 
# software, which has primitive graphviz parsing :(

print ("digraph G {\n") #+
       #"edge [dir=none]\n"
       #" ranksep=3;\n"
       #" ratio=auto;")

for link in links:
    print "%s -> %s;" % (link[0], link[1])

print "}"
