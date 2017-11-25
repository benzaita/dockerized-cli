const child_process = require('child_process')
const fs = require('fs')
const path = require('path')
const findUp = require('dnif')
const debug = require('debug')('builder:exec')

function readConfig(baseDir) {
  return JSON.parse(fs.readFileSync(`${baseDir}/.builder/config.json`))
}

function findBaseDir() {
  return new Promise((resolve, reject) => {
    findUp({
      name: '.builder',
      startPath: process.cwd()
    },
    (err, dir) => {
      if (err) {
        reject(new Error(err))
      }
      resolve(dir)
    })
  })
}

function execInDockerCompose(command, baseDir, dockerComposeFile) {
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

module.exports = async function exec(argv) {
  const command = process.argv.slice(3).join(' ')
  const baseDir = await findBaseDir()
  debug(`found .builder in ${baseDir}`)
  const config = readConfig(baseDir)
  const dockerComposeFile = config.composeFile

  execInDockerCompose(command, baseDir, dockerComposeFile)
}
