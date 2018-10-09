const findBaseDir = require('../utils/find-base-dir')
const readConfig = require('../utils/read-config')()
const prettifyErrors = require('../utils/prettify-errors')
const execFactory = require('../operations/exec')

module.exports = {
  command: 'shell',
  desc: 'drop into an interactive shell inside the dockerized',
  builder: yargs => yargs,
  handler: async () => {
    const baseDir = await findBaseDir()
    const config = readConfig(baseDir)
    const exec = execFactory({ config, baseDir })

    prettifyErrors(async () => {
      const command = '/bin/sh'
      const completion = await exec(command)
      process.exit(completion.code)
    })()
  }
}
