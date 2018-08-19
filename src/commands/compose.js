const findBaseDir = require('../utils/find-base-dir')
const readConfig = require('../utils/read-config')
const prettifyErrors = require('../utils/prettify-errors')
const DockerCompose = require('../utils/docker-compose')

function execDockerComposeCommand(command, baseDir, dockerComposeFile) {
  DockerCompose.spawn({
    baseDir,
    dockerComposeFile,
    _dockderComposeArgs: command
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
