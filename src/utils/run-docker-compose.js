const childProcess = require('child_process')
const path = require('path')
const debug = require('debug')('dockerized:docker-compose')
const Completion = require('./completion')

const runDockerCompose = ({
  baseDir,
  dockerComposeFile,
  dockerComposeArgs,
  rejectOnNonZeroExitCode
}) => {
  const args = [
    '-f',
    path.resolve(baseDir, dockerComposeFile),
    ...dockerComposeArgs
  ]

  debug(`running: docker-compose ${args.join(' ')}`)
  return new Promise((resolve, reject) => {
    const child = childProcess.spawn('docker-compose', args, {
      stdio: 'inherit'
    })

    child.on('exit', code => {
      debug(`child process exited with code ${code}`)
      if (code !== 0 && rejectOnNonZeroExitCode) {
        reject(Completion.of(code))
      } else {
        resolve(Completion.of(code))
      }
    })
  })
}

module.exports = runDockerCompose
