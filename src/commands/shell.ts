import { Command, flags } from '@oclif/command';
import findBaseDir from '../utils/find-base-dir';
import createReadConfig from '../utils/read-config';
import prettifyErrors from '../utils/prettify-errors';
import execFactory from '../operations/exec';

const readConfig = createReadConfig();

export default class Shell extends Command {
    public static description = 'drop into an interactive shell inside the dockerized';

    public async run() {
        const baseDir = await findBaseDir();
        const config = readConfig(baseDir);
        const exec = execFactory({
            runDockerCompose: undefined,
            runInContainer: undefined,
            writeConfig: undefined,
            config,
            baseDir,
        });

        prettifyErrors(async () => {
            const command = '/bin/sh';
            const completion = await exec(command);
            process.exit(completion.getCode());
        })();
    }
}
