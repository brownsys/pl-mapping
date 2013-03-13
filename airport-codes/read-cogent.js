var fs = require('fs')
var _ = require('underscore')
var cheerio = require('cheerio')
var a = require('assert')

var cdc =
  _.range(1, 3+1)
  .map(function(n) {
    return './' + n + '.txt'
  })

var ndc =
  _.range(1, 32+1)
  .map(function(n) {
    return './' + n + '-of32.txt'
  })

cdc = cdc.concat(ndc)

var results =
  cdc.map(function(filename) {
    var html = fs.readFileSync(filename, 'utf8');
    $ = cheerio.load(html)
    var data = parse($)
    console.log(data.length)
    return data
  });

results = _.flatten(results)
console.log(results.length)

fs.writeFileSync('./datacenters.json', JSON.stringify(results), 'utf8')

function parse($) {
  var table = $('.servloc-results')
  var headers =
    table.children('th')
    .map(function(i, header) {
      return $(header).text()
        .toLowerCase()
        .replace(' ', '', 'g')
        .replace(',', '', 'g')
    })

  var rows =
    table.children('tr').map(function(i, tr) {
      var tds = $(tr).children('td')
      a.equal(tds.length, headers.length)
      a.ok(tds.first().text() === 'CDC' || tds.first().text() === 'CNDC')

      var row = {}
      tds.each(function(j, td) {
        row[headers[j]] = $(td).text()
      })
      return row
    })
  return rows
}
