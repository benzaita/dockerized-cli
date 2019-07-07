import fingerprintConfig from '../utils/fingerprint-config';
import createDebug from 'debug';
import _runInContainer from '../utils/run-in-container';
import _runDockerCompose from '../utils/run-docker-compose';
import _writeConfig from '../utils/write-config';
import { Config } from '../utils/read-config';
import Completion from '../utils/completion';

const debug = createDebug('dockerized:exec');

export interface CreateExecInput {
    config: Config;
    baseDir: string;
    runInContainer?: typeof _runInContainer;
    runDockerCompose?: typeof _runDockerCompose;
    writeConfig?: typeof _writeConfig;
}

export default function createExec({
    config,
    baseDir,
    runInContainer = _runInContainer,
    runDockerCompose = _runDockerCompose,
    writeConfig = _writeConfig,
}: CreateExecInput) {
    return async (command: string): Promise<Completion> => {
        const dockerComposeFile = config.composeFile;
        const currentConfigFingerprint = fingerprintConfig(config);
        const rebuildInDockerCompose = () =>
            runDockerCompose({
                dockerComposeArgs: ['build'],
                baseDir,
                dockerComposeFile,
                rejectOnNonZeroExitCode: true,
            });

        if (currentConfigFingerprint !== config.fingerprint) {
            const configWithFingerprint = Object.assign({}, config, {
                fingerprint: currentConfigFingerprint,
            });

            debug(`config.fingerprint is outdated. running 'compose build'`);
            await rebuildInDockerCompose();

            debug(`updating config.fingerprint`);
            writeConfig(baseDir, configWithFingerprint);
        }

        const completion = await runInContainer({
            command,
            baseDir,
            dockerComposeFile,
            rejectOnNonZeroExitCode: false,
        });
        return completion;
    };
}
