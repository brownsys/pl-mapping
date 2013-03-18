# airport-codes scripts

# the flow

`atlas-faa.txt` contains all the airport codes seen in DNS entries

`atlas-to-latlong.js` takes the DNS codes and looks them up on
world-airport-codes.com. The lat and long for each code are then put into
`output-atlas-with-latlong.json`.

NOTE: `cat output-atlas-with-latlong.json | json -k -a | wc -l`
Should return 170 or greater! (There are 170 airport codes, as you can see in
`atlas-faa.txt`)

### now we have lat and long for each airport code!

Next we map them...

NOTE: There are about 17 codes that do not correspond to an airport, as far as we know.

TODO
