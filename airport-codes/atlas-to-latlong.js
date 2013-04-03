var a = require('assert')
var fs = require('fs')
var _ = require('underscore')
var async = require('async')
var csv = require('csv')
var request = require('request')
var identity = function (s) { return s };

// http://www.world-airport-codes.com/search/?Submit=1&criteria=jfk
var url = "http://www.world-airport-codes.com/search/?Submit=1&criteria="

// these are the airport codes seen in DNS data
var cogentcodes = require('./atlas-codes')

// for testing
// cogentcodes = [
//   'zag',  // exists, utf8 redirect issue though!
//   'jfk', // exists
//   'lon' // doesnt exist
// ]

var airport2latlong = {}

async.each(cogentcodes, function(code, cb) {
  var uri = url + code
  console.log('Reading', uri)
  request(uri, function(error, response, body) {
    if (!error && response.statusCode == 200) {
      airport2latlong[code] = parse(body)
      airport2latlong[code].url = uri
      return cb()
    }
    console.log(error, response.statusCode)
    console.log('Error caused by utf8 redirect error in their website.')
    if (code === 'lon') {
      airport2latlong[code] = {
        lat: 51.507222,
        lon: -0.1275,
        url: "London special case"
      }
    }
    if (code === 'qzo') {
      airport2latlong[code] = {
        lat: 43.45589828491211,
        lon: 11.84700012207031,
        url: "http://airportdatabase.net/italy/arezzo-airport_29439.html"
      }
    }
    if (code === 'zag') {
      console.log("Fixed the problem for zag!")
      // let's fix it.
      airport2latlong[code] = {
        lat: 45.743055555556,
        lon: 16.068888888889,
        url: "http://www.world-airport-codes.com/croatia-(hrvatska)/zra%C4%8Dna-luka-zagreb-7829.html"
      }
      return cb()
    }
    return cb(error)
  })
}, done)

function parse(body) {
  if (~body.indexOf('<h1>Search Results for "')) {
    return {
      lat: null
    , lon: null
    }
  }

  var startFragment = 'new L.LatLng('
  var startIndex = body.indexOf(startFragment)
  a.ok(startIndex);

  var start = startIndex + startFragment.length

  body = body.substring(start); // get rid of junk at the beginning

  // the next paren
  var end = body.indexOf(')')
  a.ok(end)
  var raw = body.substring(0, end)
  var tuple = raw.split(', ')

  var lat = tuple[0]
  var lon = tuple[1]
  a.ok(lat) // strings should have length
  a.ok(lon)

  lat = parseFloat(lat, 10)
  lon = parseFloat(lon, 10)
  a.ok(!isNaN(lat)) // should be numbers
  a.ok(!isNaN(lon))

  return {
    lat: lat
  , lon: lon
  }
}

function done(err) {
  if (err) console.log(err)

  console.log(airport2latlong)
  fs.writeFileSync('./output-atlas-with-latlong.json'
    , JSON.stringify(airport2latlong))
  console.log('done')
}
