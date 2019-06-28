import findBaseDir from '../utils/find-base-dir';
import createReadConfig from '../utils/read-config';
import prettifyErrors from '../utils/prettify-errors';
import execFactory from '../operations/exec';

const readConfig = createReadConfig();

export default {
    command: 'shell',
    desc: 'drop into an interactive shell inside the dockerized',
    builder: yargs => yargs,
    handler: async () => {
        const baseDir = await findBaseDir();
        const config = readConfig(baseDir);
        const exec = execFactory({ config, baseDir });

        prettifyErrors(async () => {
            const command = '/bin/sh';
            const completion = await exec(command);
            process.exit(completion.code);
        })();
    },
};
