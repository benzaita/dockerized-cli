const debug = require('debug')('builder:exec')
const _runInContainer = require('../utils/run-in-container')
const _runDockerCompose = require('../utils/run-docker-compose')
const _writeConfig = require('../utils/write-config')
const fingerprint = require('../utils/fingerprint-config')

module.exports = ({
  config,
  baseDir,
  runInContainer = _runInContainer,
  runDockerCompose = _runDockerCompose,
  writeConfig = _writeConfig
}) => async command => {
  const dockerComposeFile = config.composeFile
  const currentConfigFingerprint = fingerprint(config)
  const rebuildInDockerCompose = () =>
    runDockerCompose({
      dockerComposeArgs: ['build'],
      baseDir,
      dockerComposeFile,
      rejectOnNonZeroExitCode: true
    })

  if (currentConfigFingerprint !== config.fingerprint) {
    const configWithFingerprint = Object.assign({}, config, {
      fingerprint: currentConfigFingerprint
    })

    debug(`config.fingerprint is outdated. running 'compose build'`)
    await rebuildInDockerCompose()

    debug(`updating config.fingerprint`)
    writeConfig(baseDir, configWithFingerprint)
  }

  const completion = await runInContainer({
    command,
    baseDir,
    dockerComposeFile
  })
  return completion
}
