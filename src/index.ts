import yargs from 'yargs';

import exec from './commands/exec';
import init from './commands/init';
import compose from './commands/compose';
import shell from './commands/shell';
import clean from './commands/clean';

yargs
    .usage('dockerized COMMAND')
    .command(exec)
    .command(init)
    .command(compose)
    .command(shell)
    .command(clean)
    .demandCommand()
    .help().argv;
