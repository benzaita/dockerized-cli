const debug = require('debug')('dockerized:read-config')
const fs = require('fs')
const path = require('path')
const md5 = require('md5')
const R = require('ramda')
const yaml = require('js-yaml')

module.exports = ({ readFile = fs.readFileSync } = {}) => baseDir => {
  const pathJoinSafe = (...parts) =>
    parts.some(part => part === undefined) ? undefined : path.join(...parts)

  const md5Safe = message => (message === undefined ? undefined : md5(message))

  const readFileSafe = filePath => {
    if (!filePath) return undefined

    debug('reading file', filePath)
    try {
      return readFile(path.join(baseDir, filePath))
    } catch (error) {
      debug(error)
      return undefined
    }
  }

  const config = JSON.parse(
    readFileSafe(path.join('.dockerized', 'config.json'))
  )

  const composeFileString = readFileSafe(config.composeFile)
  config.composeFileFingerprint = md5Safe(composeFileString)

  const composeFileJson = yaml.safeLoad(composeFileString)
  const dockerFilePath = R.path(
    ['services', 'dockerized', 'build', 'dockerfile'],
    composeFileJson
  )
  const dockerFileString = readFileSafe(
    pathJoinSafe('.dockerized', dockerFilePath)
  )
  config.dockerFileFingerprint = md5Safe(dockerFileString)

  return config
}
