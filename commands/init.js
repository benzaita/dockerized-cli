const fs = require('fs')
const yaml = require('js-yaml')
const prettifyErrors = require('../utils/prettify-errors')

const composeConfig = {
  version: '2',
  services: {
    builder: {
      image: 'busybox',
      entrypoint: [
        'sh',
        '-c'
      ],
      environment: [],
      volumes: [],
    }
  },
  volumes: {}
}

module.exports = {
  command: 'init',
  desc: 'initialize builder in this directory',
  builder: yargs => yargs
    .option('f', {
      alias: 'file',
      default: 'docker-compose.builder.yml',
      describe: 'Docker-Compose file to use',
      type: 'string'
    })
    .option('y', {
      alias: 'withYarnCache',
      describe: 'Includes support for utilizing yarn cache',
      type: 'boolean'
    })
    .option('d', {
      alias: 'withNestedDocker',
      describe: 'Includes support for running Docker inside Docker',
      default: true,
      type: 'boolean'
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

    if (argv.withYarnCache) {
      composeConfig.services.builder.volumes.push('yarn-cache:/data/yarn-cache')
      composeConfig.services.builder.environment.push('YARN_CACHE_FOLDER=/data/yarn-cache')
      composeConfig.volumes['yarn-cache'] = {}
    }

    if (argv.withNestedDocker) {
      composeConfig.services.builder.volumes.push('/var/run/docker.sock:/var/run/docker.sock')
      composeConfig.services.builder.network_mode = 'host'
    }

    fs.writeFileSync(config.composeFile, yaml.safeDump(composeConfig))
    console.error(`created ${config.composeFile}`)
  })
}
