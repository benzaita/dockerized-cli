const fs = require('fs')
const path = require('path')
const yaml = require('js-yaml')
const prettifyErrors = require('../utils/prettify-errors')

const composeConfig = {
  version: '2',
  services: {
    cenv: {
      build: {
        context: '.'
      },
      entrypoint: ['sh', '-c'],
      environment: [],
      volumes: []
    }
  },
  volumes: {}
}

const dockerConfig = `
FROM busybox
# install your build dependencies here
`

module.exports = {
  command: 'init',
  desc: 'initialize cenv in this directory (see also: init --help)',
  builder: yargs =>
    yargs
      .option('C', {
        alias: 'composeFile',
        default: '.cenv/docker-compose.cenv.yml',
        describe: 'Docker-Compose file to create',
        type: 'string'
      })
      .option('D', {
        alias: 'dockerFile',
        default: '.cenv/Dockerfile.cenv',
        describe: 'Dockerfile to create',
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
  handler: prettifyErrors(argv => {
    const config = {
      composeFile: argv.composeFile
    }

    if (fs.existsSync('.cenv')) {
      throw new Error('already initialized')
    }

    if (fs.existsSync(argv.composeFile)) {
      throw new Error(
        `will not overwrite ${
          argv.composeFile
        }. Use --composeFile to choose a different name`
      )
    }

    if (fs.existsSync(argv.dockerFile)) {
      throw new Error(
        `will not overwrite ${
          argv.dockerFile
        }. Use --dockerFile to choose a different name`
      )
    }

    fs.mkdirSync('.cenv')
    fs.writeFileSync('.cenv/config.json', JSON.stringify(config, null, 2))

    composeConfig.services.cenv.build.dockerfile = path.relative(
      path.dirname(argv.composeFile),
      argv.dockerFile
    )

    if (argv.withYarnCache) {
      composeConfig.services.cenv.volumes.push('yarn-cache:/data/yarn-cache')
      composeConfig.services.cenv.environment.push(
        'YARN_CACHE_FOLDER=/data/yarn-cache'
      )
      composeConfig.volumes['yarn-cache'] = {}
    }

    if (argv.withNestedDocker) {
      composeConfig.services.cenv.volumes.push(
        '/var/run/docker.sock:/var/run/docker.sock'
      )
      composeConfig.services.cenv.network_mode = 'host'
    }

    fs.writeFileSync(config.composeFile, yaml.safeDump(composeConfig))

    fs.writeFileSync(argv.dockerFile, dockerConfig)

    console.error(`created ${argv.composeFile}`)
    console.error(`created ${argv.dockerFile}`)
    console.error(`hint: edit ${argv.dockerFile} to set up your container`)
  })
}
