const fs = require('fs')
const prettifyErrors = require('../utils/prettify-errors')

const composeFileTemplate = `
version: '2'
services:
  # Keep this name so builder can find it
  builder:
    # Use whatever image you want
    image: hub.int.klarna.net/exp/jenkins-agent:latest
    # Keep this so builder can exec commands inside the container
    entrypoint:
      - "sh"
      - "-c"
    # Keep this to be able to run nested docker
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    network_mode: host
`

module.exports = {
  command: 'init',
  desc: 'initialize builder in this directory',
  builder: yargs => yargs
    .option('f', {
      alias: 'file',
      default: 'docker-compose.builder.yml',
      describe: 'Docker-Compose file to use',
      type: 'string'
    }),
  handler: prettifyErrors(function init(argv) {
    const config = {
      composeFile: argv.file
    }

    if (fs.existsSync('.builder')) {
      throw new Error('already initialized')
    }

    if (fs.existsSync(config.composeFile)) {
      throw new Error(`will not overwrite ${config.composeFile}. Use --file to choose a different name`)
    }

    fs.mkdirSync('.builder')
    fs.writeFileSync('.builder/config.json', JSON.stringify(config, null, 2))
    console.error('created .builder/')

    fs.writeFileSync(config.composeFile, composeFileTemplate)
    console.error(`created ${config.composeFile}`)
  })
}
