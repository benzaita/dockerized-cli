#!/usr/bin/env node

const yargs = require("yargs");

const argv = yargs
  .usage("builder COMMAND")
  .command(require("./commands/exec"))
  .command(require("./commands/init"))
  .command(require("./commands/compose"))
  .command(require("./commands/shell"))
  .command(require("./commands/clean"))
  .demandCommand()
  .help().argv;
