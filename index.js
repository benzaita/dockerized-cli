const yargs = require('yargs')
const init = require('./commands/init')
const exec = require('./commands/exec')

const prettifyErrors = fn => argv => {
  try {
    fn(argv)
  } catch(e) {
    console.error(e.message)
    process.exit(1)
  }
}

const argv = yargs
  .usage('builder COMMAND')
  .command(
    'init',
    'initialize builder in this directory',
    yargs => yargs
      .option('f', {
        alias: 'file',
        default: 'docker-compose.builder.yml',
        describe: 'Docker-Compose file to use',
        type: 'string'
      }),
    prettifyErrors(init)
  )
  .command({
    command: 'exec',
    desc: 'execute a command inside the builder',
    builder: yargs => yargs,
    handler: prettifyErrors(exec)
  })
  .demandCommand()
  .help()
  .argv

