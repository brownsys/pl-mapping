var fs = require('fs')
var csv = require('csv')
var _ = require('underscore')

// these are the airport codes seen in DNS data
var cogentcodes =
  fs.readFileSync('./atlas-faa.txt', 'utf8')
  .split('\n')
  .map(function(line) {
    line = line.trim()
    return line.split(' ')[0].toLowerCase()
  });

var allcodes = []

csv().from(fs.readFileSync('./airports.csv', 'utf8'))

// 0 Airport ID  Unique OpenFlights identifier for this airport.
// 1 Name        Name of airport. May or may not contain the City name.
// 2 City        Main city served by airport. May be spelled differently from Name.
// 3 Country     Country or territory where airport is located.
// 4 IATA/FAA
// 5 ICAO
// 6 Latitude
// 7 Longitude
// 8 Altitude    In feet.
// 9 Timezone
.on('record', function(row, index) {
  // console.log('#'+index+' '+JSON.stringify(row));
  var name = row[1].trim()
  var faa = row[4].trim()
  var icao = row[5].trim().replace('\\N', '')
  var code = faa || icao;
  // console.log(code || '---', name)
  if (code) allcodes.push(code.toLowerCase())

}).on('end', function(count) {
  // console.log('All the airport codes: ' + allcodes.join(' '))

  // console.log('Cogent\'s codes: ' + cogentcodes.join(' '))

  fs.writeFileSync('./output-cogent-codes.txt'
    , cogentcodes.join('\n'))

  // console.log('\nCogent codes not found in the airports.csv:')
  fs.writeFileSync('./output-codes-not-in-airports-csv.txt'
    , _.difference(cogentcodes, allcodes).join('\n'))

  console.log('Done. See', './output-cogent-codes.txt', 'and'
    , './output-codes-not-in-airports-csv.txt')
})
