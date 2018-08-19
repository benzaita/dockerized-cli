const findBaseDir = require('../utils/find-base-dir')
const readConfig = require('../utils/read-config')()
const prettifyErrors = require('../utils/prettify-errors')
const runDockerCompose = require('../utils/run-docker-compose')

function execDockerComposeCommand(command, baseDir, dockerComposeFile) {
  runDockerCompose({
    baseDir,
    dockerComposeFile,
    dockerComposeArgs: command
  })
}

module.exports = {
  command: 'compose',
  desc: 'run a docker-compose command',
  builder: yargs => yargs,
  handler: prettifyErrors(async () => {
    const command = process.argv.slice(3)
    const baseDir = await findBaseDir()
    const config = readConfig(baseDir)
    const dockerComposeFile = config.composeFile

    execDockerComposeCommand(command, baseDir, dockerComposeFile)
  })
}
