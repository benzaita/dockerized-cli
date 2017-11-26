const child_process = require('child_process')
const path = require('path')
const debug = require('debug')('builder:compose')
const findBaseDir = require('../utils/find-base-dir')
const readConfig = require('../utils/read-config')
const prettifyErrors = require('../utils/prettify-errors')

function execDockerComposeCommand(command, baseDir, dockerComposeFile) {
  const args = [
    '-f', path.resolve(baseDir, dockerComposeFile),
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

module.exports = {
  command: 'compose',
  desc: 'run a docker-compose command',
  builder: yargs => yargs,
  handler: prettifyErrors(async function exec(argv) {
    const command = process.argv.slice(3).join(' ')
    const baseDir = await findBaseDir()
    const config = readConfig(baseDir)
    const dockerComposeFile = config.composeFile

    execDockerComposeCommand(command, baseDir, dockerComposeFile)
  })
}