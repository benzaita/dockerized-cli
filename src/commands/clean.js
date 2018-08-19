const findBaseDir = require('../utils/find-base-dir')
const readConfig = require('../utils/read-config')()
const prettifyErrors = require('../utils/prettify-errors')
const runDockerCompose = require('../utils/run-docker-compose')

module.exports = {
  command: 'clean',
  desc: 'removes the container',
  builder: yargs => yargs,
  handler: prettifyErrors(async () => {
    const baseDir = await findBaseDir()
    const config = readConfig(baseDir)
    const dockerComposeFile = config.composeFile

    runDockerCompose({
      baseDir,
      dockerComposeFile,
      dockerComposeArgs: ['down']
    })
  })
}
