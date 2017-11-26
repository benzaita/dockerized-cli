const yargs = require('yargs')

const argv = yargs
  .usage('builder COMMAND')
  .command(require('./commands/exec'))
  .command(require('./commands/init'))
  .command(require('./commands/compose'))
  .demandCommand()
  .help()
  .argv

