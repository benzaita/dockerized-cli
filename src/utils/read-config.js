const debug = require('debug')('builder:read-config')
const fs = require('fs')
const md5 = require('md5')

module.exports = ({ readFile = fs.readFileSync } = {}) => baseDir => {
  const config = JSON.parse(readFile(`${baseDir}/.builder/config.json`))

  try {
    const composeFile = readFile(`${baseDir}/${config.composeFile}`)
    config.composeFileFingerprint = md5(composeFile)
  } catch (error) {
    debug(error)
  }

  return config
}
