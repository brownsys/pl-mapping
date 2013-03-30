#!/usr/bin/python

import sys

# Get Cisco model from abbrevation
# Map from: http://cpansearch.perl.org/src/KBRINT/Cisco-Abbrev-0.02/lib/Cisco/Abbrev.pm
#
# Juniper listing: http://www.juniper.net/techpubs/software/junos-security/junos-security10.0/junos-security-swconfig-interfaces-and-routing/network-interfaces-section.html
def get_model(model_abbr):
	abbreviations = {
		'fa': 'FastEthernet',
		'gi': 'GigabitEthernet',
		'te': 'TenGigabitEthernet',
		'et': 'Ethernet',
		'vl': 'Vlan',
		'fd': 'Fddi',
		'is': 'IntegratedServicesModule',
		#'portch': 'Port-channel',
		#'po': 'Port-channel',

		'tu': 'Tunnel',
		'lo': 'Loopback',
		'vi': 'Virtual-Access',
		'vt': 'Virtual-Template',
		'eo' : 'EOBC',

		'se': 'Serial',
		'Se': 'Serial',
		'po': 'POS',
		'posch': 'Pos-channel',
		'mu': 'Multilink',
		'at': 'ATM',

		'async': 'Async',
		'group-async': 'Group-Async',
		'mfr': 'MFR'
	}

	try:
		return abbreviations[model_abbr]
	except KeyError:
		return "(unknown)"

	

for line in sys.stdin.readlines():
	(ip_side, host_side) = line.split(" domain name pointer ")
	
	ip_parts = ip_side.split(".")
	ip = ip_parts[3] + "." + ip_parts[2] + "." + ip_parts[1] + "." + ip_parts[0]

	model = get_model(host_side[0:2])

	if host_side[0:4] == "giga":
		model = "(unknown)"

	if host_side[0:3] == "tel":
		model = "(unknown)"
	
	if host_side[0:3] == "isc":
		model = "(unknown)"

	if host_side[0:3] == "att":
		model = "(unknown)"
	
	tmp = host_side[:-2].split(".")[:-3]
	tmp.reverse()
	for part in tmp:
		print(part + "\t"),
	
	if len(tmp) < 3:
		print("\t"),

	print(host_side[:-2] + "\t"),
	print(ip + "\t"),
	print(model)
