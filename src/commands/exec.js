import execFactory from '../operations/exec';
import prettifyErrors from '../utils/prettify-errors';
import findBaseDir from '../utils/find-base-dir';
import createReadConfig from '../utils/read-config';

const readConfig = createReadConfig();

const epilog = `
Environment variables:
  To provide environment variables, either add them in the docker-compose
  file or pass them in the command line:

  dockerized exec FOO=1 BAR=2 COMMAND
`;

export default {
    command: 'exec.ts',
    desc: 'execute a command inside the dockerized',
    builder: yargs => yargs.epilog(epilog),
    handler: async () => {
        const baseDir = await findBaseDir();
        const config = readConfig(baseDir);
        const exec = execFactory({ config, baseDir });

        prettifyErrors(async () => {
            const command = process.argv.slice(3).join(' ');
            const completion = await exec(command);
            process.exit(completion.code);
        })();
    },
};
