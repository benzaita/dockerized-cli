const findBaseDir = require('../utils/find-base-dir')
const readConfig = require('../utils/read-config')
const prettifyErrors = require('../utils/prettify-errors')
const execInDockerCompose = require('../utils/exec-in-docker-compose')

module.exports = {
  command: 'shell',
  desc: 'drop into an interactive shell inside the builder',
  builder: yargs => yargs,
  handler: prettifyErrors(async function exec(argv) {
    const command = '/bin/sh'
    const baseDir = await findBaseDir()
    const config = readConfig(baseDir)
    const dockerComposeFile = config.composeFile

    execInDockerCompose(command, baseDir, dockerComposeFile)
  })
}