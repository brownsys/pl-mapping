// converts COGENT-MASTER-ATLAS.txt
// to a list of 3-letter airport codes

var fs = require('fs')
var _ = require('underscore')
var identity = function(i) { return i }

// codes that should be ignored, b/c not actually for airports

var invalid = 'dev cat fev moo pro ref dem f-p f-t lng fix b01 hq0 na0 not pai'.split(' ')

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

    // For several major cities, Cogent uses the
    // metropolitan airport code, rather than the specific code
    // NOTE: London is there as 'lon' but Heathrow is actually being used for Slough, England
    if (code === 'rom') code = 'fco' // Rome
    if (code === 'mil') code = 'mxp' // Milan
    if (code === 'par') code = 'cdg' // Paris
    if (code === 'tyo') code = 'nrt' // Tokyo
    if (code === 'sto') code = 'arn' // Stockholm
    return code
  })
  .filter(identity)
  .sort()
)

if (!module.parent) {
  console.log(module.exports)
  console.log(module.exports.length)
}
