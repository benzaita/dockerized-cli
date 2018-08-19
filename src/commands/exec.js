const findBaseDir = require('../utils/find-base-dir')
const readConfig = require('../utils/read-config')
const prettifyErrors = require('../utils/prettify-errors')
const execInDockerCompose = require('../utils/exec-in-docker-compose')

const epilog = `
Environment variables:
  To provide environment variables, either add them in the docker-compose
  file or pass them in the command line:

  builder exec FOO=1 BAR=2 COMMAND
`

module.exports = {
  command: 'exec',
  desc: 'execute a command inside the builder',
  builder: yargs => yargs.epilog(epilog),
  handler: prettifyErrors(async () => {
    const command = process.argv.slice(3).join(' ')
    const baseDir = await findBaseDir()
    const config = readConfig(baseDir)
    const dockerComposeFile = config.composeFile

    execInDockerCompose(command, baseDir, dockerComposeFile)
  })
}
