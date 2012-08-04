#!/usr/bin/python

import xmlrpclib, sys, time

api_server = xmlrpclib.ServerProxy("https://www.planet-lab.org/PLCAPI/")
api_calls = 0 

sys.stderr.write("Username: ")
username = sys.stdin.readline()[:-1]
sys.stderr.write("Password: ")
password = sys.stdin.readline()[:-1]
sys.stderr.write("Slice name: ")
slice_name = sys.stdin.readline()[:-1]

auth = {}
auth['Username'] = username 
auth['AuthString'] = password
auth['AuthMethod'] = "password"

node_ids = api_server.GetSlices(auth, {'name': slice_name}, ['node_ids'])[0]['node_ids']
api_calls += 1
time.sleep(1)

for node_id in node_ids:
	print api_server.GetNodes(auth, node_id, ['hostname'])[0]['hostname']
	api_calls += 1
	time.sleep(1)

	# Maximum rate of API calls is 50 per 5 minutes
	if (api_calls == 50):
		time.sleep(255)
		api_calls = 0
