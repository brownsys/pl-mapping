// converts COGENT-MASTER-ATLAS.txt
// to a list of 3-letter airport codes

var fs = require('fs')
var _ = require('underscore')
var identity = function(i) { return i }

// codes that should be ignored, b/c not actually for airports

var invalid = 'dev cat fev moo pro ref dem f-p f-t lng fix'.split(' ')

module.exports =
_.uniq(
  // fs.readFileSync('./atlas-faa.txt', 'utf8')
  fs.readFileSync('./COGENT-MASTER-ATLAS.txt', 'utf8')
  .trim()
  .split('\n')
  .map(function(line) {
    line = line.trim()
    var first = line.split(' ')[0].toLowerCase()
    var code = first.substring(0, 3)
    if (~invalid.indexOf(code)) return

    // rome is not in world-airport-codes
    if (code === 'rom') code = 'fco'
    return code
  })
  .filter(identity)
  .sort()
)

if (!module.parent) {
  console.log(module.exports)
  console.log(module.exports.length)
}
