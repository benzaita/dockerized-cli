const fs = require('fs')

module.exports = function readConfig(baseDir) {
  return JSON.parse(fs.readFileSync(`${baseDir}/.builder/config.json`))
}
