const findBaseDir = require('../utils/find-base-dir')
const readConfig = require('../utils/read-config')
const prettifyErrors = require('../utils/prettify-errors')
const DockerCompose = require('../utils/docker-compose')

module.exports = {
  command: 'clean',
  desc: 'removes the container',
  builder: yargs => yargs,
  handler: prettifyErrors(async function exec(argv) {
    const baseDir = await findBaseDir()
    const config = readConfig(baseDir)
    const dockerComposeFile = config.composeFile

    DockerCompose.spawn({
      baseDir,
      dockerComposeFile,
      dockderComposeArgs: ['down']
    })
  })
}