# airport-codes scripts

To set up the environment, install <http://nodejs.org>, and then run

```
cd this-project/

ls # you should see the package.json file

npm install # this installs dependencies
```

## converting `atlas-faa.txt` airport codes into lat and long

`atlas-faa.txt` contains all the airport codes seen in DNS entries

`node atlas-to-latlong.js` takes the DNS codes and looks them up on
world-airport-codes.com. The lat and long for each code are then put into
`output-atlas-with-latlong.json`.

NOTE: `cat output-atlas-with-latlong.json | json -k -a | wc -l`
Should return 170 or greater! (There are 170 airport codes, as you can see in
`atlas-faa.txt`)

### now we have lat and long for each airport code!

Next we map them...

NOTE: There are about 17 codes that do not correspond to an airport, as far as we know.

TODO


## cogent.com provides datacenter locations
`node read-cogent.js` scrapes cogent's site and pulls down the locations of all
their datacenters into `datacenters.json`
