import { Command } from '@oclif/command';
import findBaseDir from '../utils/find-base-dir';
import createReadConfig from '../utils/read-config';
import prettifyErrors from '../utils/prettify-errors';
import runDockerCompose from '../utils/run-docker-compose';

const readConfig = createReadConfig();

export default class Clean extends Command {
    public static description = 'removes the container';

    public static examples = [`$ dockerized clean`];

    public async run() {
        return prettifyErrors(async () => {
            const baseDir = await findBaseDir();
            const config = readConfig(baseDir);
            const dockerComposeFile = config.composeFile;

            return runDockerCompose({
                baseDir,
                dockerComposeFile,
                dockerComposeArgs: ['down'],
                rejectOnNonZeroExitCode: false,
            });
        })();
    }
}
