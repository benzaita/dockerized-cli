const child_process = require('child_process')
const path = require('path')
const debug = require('debug')('builder:exec')

module.exports = function execInDockerCompose(command, baseDir, dockerComposeFile) {
  const args = [
    '-f', path.resolve(baseDir, dockerComposeFile),
    'run',
    '--rm',
    '-v', `${baseDir}:${baseDir}`,
    '-w', process.cwd(),
    'builder',
    command
  ]

  debug(`running: docker-compose ${args.join(' ')}`)
  const child = child_process.spawn('docker-compose', args, {
    stdio: 'inherit'
  })

  child.on('exit', code => {
    debug(`child process exited with code ${code}. propagating`)
    process.exit(code)
  })
}