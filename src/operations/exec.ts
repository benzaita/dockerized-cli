import fingerprintConfig from '../utils/fingerprint-config';
import createDebug from 'debug';
import _runInContainer from '../utils/run-in-container';
import _runDockerCompose from '../utils/run-docker-compose';
import _writeConfig from '../utils/write-config';
import { Config } from '../utils/read-config';
import Completion from '../utils/completion';
import {DefaultDockerClient, DockerClient} from "../utils/docker-client";

const debug = createDebug('dockerized:exec');

export interface CreateExecInput {
    config: Config;
    baseDir: string;
    runInContainer?: typeof _runInContainer;
    runDockerCompose?: typeof _runDockerCompose;
    dockerClient?: DockerClient;
    writeConfig?: typeof _writeConfig;
}

function isCiEnvironmentVariableEnabled(ci?: string) {
    return ci === 'true' || ci === '1' || ci === 'yes' || ci === 'on';
}

export default function createExec({
    config,
    baseDir,
    runInContainer = _runInContainer,
    runDockerCompose = _runDockerCompose,
    dockerClient = new DefaultDockerClient(),
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

        if (config.cacheImage) {
            debug('looking for config.cacheImage locally', config.cacheImage)
            const imageExistsLocally = await dockerClient.imageExistsLocally(config.cacheImage);
            if (!imageExistsLocally) {
                debug(`config.cacheImage not found locally. pulling`, config.cacheImage)
                await runDockerCompose({
                    dockerComposeArgs: ['pull', 'dockerized'],
                    baseDir,
                    dockerComposeFile,
                    rejectOnNonZeroExitCode: false
                });
            }
        }

        if (currentConfigFingerprint !== config.fingerprint) {
            const configWithFingerprint = Object.assign({}, config, {
                fingerprint: currentConfigFingerprint,
            });

            debug(`config.fingerprint is outdated. running 'compose build'`);
            await rebuildInDockerCompose();

            debug(`updating config.fingerprint`);
            writeConfig(baseDir, configWithFingerprint);

            if (config.cacheImage) {
                if (isCiEnvironmentVariableEnabled(process.env.CI)) {
                    debug(`not pushing config.cacheImage because CI='${process.env.CI}'`, config.cacheImage);
                } else {
                    debug(`image updated. pushing config.cacheImage`, config.cacheImage);
                    await runDockerCompose({
                        dockerComposeFile,
                        baseDir,
                        dockerComposeArgs: ['push', 'dockerized'],
                        rejectOnNonZeroExitCode: false
                    })
                }
            }
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
