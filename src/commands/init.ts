import { Command, flags } from '@oclif/command';
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import prettifyErrors from '../utils/prettify-errors';

const composeConfig = {
    version: '2',
    services: {
        dockerized: {
            build: {
                context: '.',
                dockerfile: '',
            },
            entrypoint: ['sh', '-c'],
            environment: [] as string[],
            volumes: [] as string[],
        },
    },
    volumes: {},
};

const dockerConfig = `
FROM busybox
# install your build dependencies here
`;

export default class Init extends Command {
    public static description = 'initialize dockerized in this directory (see also: init --help)';

    public static examples = [`$ dockerized init`];

    public static flags = {
        composeFile: flags.string({
            description: 'Docker-Compose file to create',
            default: '.dockerized/docker-compose.dockerized.yml',
        }),
        dockerFile: flags.string({
            description: 'Dockerfile to create',
            default: '.dockerized/Dockerfile.dockerized',
        }),
        withYarnCache: flags.boolean({
            description: 'Includes support for utilizing yarn cache',
            default: false,
        }),
        withGoCache: flags.boolean({
            description: 'Includes a volume for GOPATH',
            default: false,
        }),
        withNestedDocker: flags.boolean({
            description: 'Includes support for running Docker inside Docker',
            default: false,
        }),
    };

    public async run() {
        const { args, flags } = this.parse(Init);

        return prettifyErrors(() => {
            const config = {
                composeFile: flags.composeFile,
            };

            if (fs.existsSync('.dockerized')) {
                throw new Error('already initialized');
            }

            if (flags.composeFile === undefined || fs.existsSync(flags.composeFile)) {
                throw new Error(
                    `will not overwrite ${flags.composeFile}. Use --composeFile to choose a different name`,
                );
            }

            if (flags.dockerFile === undefined || fs.existsSync(flags.dockerFile)) {
                throw new Error(`will not overwrite ${flags.dockerFile}. Use --dockerFile to choose a different name`);
            }

            fs.mkdirSync('.dockerized');
            fs.writeFileSync('.dockerized/config.json', JSON.stringify(config, null, 2));

            composeConfig.services.dockerized.build.dockerfile = path.relative(
                path.dirname(flags.composeFile),
                flags.dockerFile,
            );

            if (flags.withYarnCache) {
                composeConfig.services.dockerized.volumes.push('yarn-cache:/data/yarn-cache');
                composeConfig.services.dockerized.environment.push('YARN_CACHE_FOLDER=/data/yarn-cache');
                // @ts-ignore
                composeConfig.volumes['yarn-cache'] = {};
            }

            if (flags.withGoCache) {
                composeConfig.services.dockerized.volumes.push('go-cache:/go');
                composeConfig.services.dockerized.environment.push('GOPATH=/go');
                // @ts-ignore
                composeConfig.volumes['go-cache'] = {};
            }

            if (flags.withNestedDocker) {
                composeConfig.services.dockerized.volumes.push('/var/run/docker.sock:/var/run/docker.sock');
                // @ts-ignore
                composeConfig.services.dockerized.network_mode = 'host';
            }

            fs.writeFileSync(config.composeFile as string, yaml.safeDump(composeConfig));

            fs.writeFileSync(flags.dockerFile, dockerConfig);

            console.error(`created ${flags.composeFile}`);
            console.error(`created ${flags.dockerFile}`);
            console.error(`hint: edit ${flags.dockerFile} to set up your container`);
        })();
    }
}
