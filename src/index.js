#!/usr/bin/env node

const yargs = require('yargs')

// eslint-disable-next-line no-unused-expressions
yargs
  .usage('builder COMMAND')
  .command(require('./commands/exec'))
  .command(require('./commands/init'))
  .command(require('./commands/compose'))
  .command(require('./commands/shell'))
  .command(require('./commands/clean'))
  .demandCommand()
  .help().argv
