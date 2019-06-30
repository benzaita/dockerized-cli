import { Command } from '@oclif/command';
import findBaseDir from '../utils/find-base-dir';
import createReadConfig from '../utils/read-config';
import prettifyErrors from '../utils/prettify-errors';
import runDockerCompose from '../utils/run-docker-compose';

const readConfig = createReadConfig();

function execDockerComposeCommand(command, baseDir, dockerComposeFile) {
    return runDockerCompose({
        rejectOnNonZeroExitCode: false,
        baseDir,
        dockerComposeFile,
        dockerComposeArgs: command,
    });
}

export default class Compose extends Command {
    public static description = 'run a docker-compose command';

    public static examples = [`$ dockerized compose ps`, `...`];

    public static strict = false;

    public async run() {
        return prettifyErrors(async () => {
            const command = this.argv;
            const baseDir = await findBaseDir();
            const config = readConfig(baseDir);
            const dockerComposeFile = config.composeFile;

            return execDockerComposeCommand(command, baseDir, dockerComposeFile);
        })();
    }
}
