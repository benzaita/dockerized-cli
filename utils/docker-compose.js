const child_process = require('child_process')
const path = require('path')
const debug = require('debug')('builder:docker-compose')

module.exports = {
  spawn({ baseDir, dockerComposeFile, dockderComposeArgs }) {
    const args = [
      '-f', path.resolve(baseDir, dockerComposeFile),
      ...dockderComposeArgs
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
}