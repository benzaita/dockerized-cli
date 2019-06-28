import findBaseDir from '../utils/find-base-dir';
import createReadConfig from '../utils/read-config';
import prettifyErrors from '../utils/prettify-errors';
import runDockerCompose from '../utils/run-docker-compose';

const readConfig = createReadConfig();

export default {
    command: 'clean.ts',
    desc: 'removes the container',
    builder: (yargs: any) => yargs,
    handler: prettifyErrors(async () => {
        const baseDir = await findBaseDir();
        const config = readConfig(baseDir);
        const dockerComposeFile = config.composeFile;

        runDockerCompose({
            baseDir,
            dockerComposeFile,
            dockerComposeArgs: ['down'],
            rejectOnNonZeroExitCode: false,
        });
    }),
};
