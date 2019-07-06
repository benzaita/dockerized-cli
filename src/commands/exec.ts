import { Command, flags } from '@oclif/command';
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

export default class Exec extends Command {
    public static description = `execute a command inside the dockerized environment
    
${epilog}`;

    public static usage = `exec [NAME=VALUE ...] COMMAND`

    public static examples = [
        `$ dockerized exec ls -l`,
        `$ dockerized exec make build`,
        `$ dockerized exec mvn`
    ]

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

        return prettifyErrors(async () => {
            const command = this.argv.join(' ');
            const completion = await exec(command);
            process.exit(completion.getCode());
        })();
    }
}
