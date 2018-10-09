const fs = require('fs')

module.exports = (baseDir, config) => {
  const configFile = `${baseDir}/.dockerized/config.json`
  fs.writeFileSync(configFile, JSON.stringify(config, null, 2))
}
