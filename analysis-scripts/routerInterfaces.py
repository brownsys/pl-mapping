import re

def getInterfaceType(intr_abbr):
	abbreviations = {
		# Physical Interfaces
		'FastEthernet': "Physical",
		'GigabitEthernet': "Physical",
		'TenGigabitEthernet': "Physical",
		'Ethernet': "Physical",
		'Fddi': "Physical",
		'ATM': "Physical",
		'POS': "Physical",
		'Serial': "Physical",
		'Serial': "Physical",
		'IntegratedServicesModule': "Physical",
		'Pos-channel': "Physical",

		# Virtual Interfaces
		'Vlan': "Virtual",
		'Multilink': "Virtual",
		'Tunnel': "Virtual",
		'Loopback': "Virtual",
		'Virtual-Access': "Virtual",
		'Virtual-Template': "Virtual",

		# Unknown Interfaces
		'EOBC': "Unknown",
		'Async': "Unknown",
		'Group-Async': "Unknown",
		'MFR': "Unknown"
	}

	try:
		return abbreviations[intr_abbr]
	except KeyError:
		return "Unknown"

"""
Takes in a COGENT-MASTER-ATLAS-FIXED.txt file for a week and
reads it to get the interface breakdown. Returns three
set of IPs, physical interfaces, virtual interfaces and unknown,
"""
def getBreakdown(masterAtlas):
	physicalInterfaces = set()
	virtualInterfaces = set()
	unknownInterfaces = set()

	# iterate through entries in file
	for line in masterAtlas.readlines():
		# split line into usuable chunks
		splitLine = re.split("\s+", line.strip());

		# only interested in first two chars
		ip = splitLine[-2]
		interfaceString = splitLine[-1]
		interfaceType = getInterfaceType(interfaceString)

		# build up sets
		if interfaceType == "Physical":
			physicalInterfaces.add(ip)
		elif interfaceType == "Virtual":
			virtualInterfaces.add(ip)
		else:
			unknownInterfaces.add(ip)
	
	return physicalInterfaces, virtualInterfaces, unknownInterfaces
