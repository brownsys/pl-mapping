TODO: steps you need to take to view the map, etc.

# airport-codes scripts

To set up the environment, install <http://nodejs.org>, and then run

```
cd this-project/

ls # you should see the package.json file

npm install # this installs dependencies
```

## converting `COGENT-MASTER-ATLAS.txt` airport codes into lat and long

`COGENT-MASTER-ATLAS.txt` contains all the airport codes seen in DNS entries

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

---

# less interesting / less relevant

## cogent.com provides datacenter locations
To download all the webpages with locations, run the following.
TODO: rewrite the script!

```sh
cd airport-codes/
for pages 1-3 of SMALL_DATACENTER_LIST
  curl URL?page=$N > $N.txt

for pages 1-32 of BIG_DATACENTER_LIST
  curl URL?page=$N > $N-of32.txt
```

`node read-cogent.js` scrapes cogent's site and pulls down the locations of all
their datacenters into `datacenters.json`

## airports.csv provides a list of mappings from airport code to location
`airports.js` counts how many of cogent's codes valid. The results of this are
written to `output-codes-not-in-airports.csv` and `output-cogent-codes`.
