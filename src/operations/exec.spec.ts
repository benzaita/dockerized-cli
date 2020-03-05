import createExec, {CreateExecInput} from './exec';
import fingerprint from '../utils/fingerprint-config';
import Completion from '../utils/completion';
import {Config} from '../utils/read-config';

const defaultConfig: Config = {
    composeFile: '',
    dockerFile: '',
    composeFileFingerprint: '',
    dockerFileFingerprint: '',
    fingerprint: '',
    cacheImage: '',
};

const withOutdatedFingerprint = (config: Config): Config =>
    Object.assign({}, config, {
        fingerprint: 'FOO',
    });

const withUpToDateFingerprint = (config: Config): Config =>
    Object.assign({}, config, {
        fingerprint: fingerprint(config),
    });

const withCacheImage = (config: Config, cacheImage: string): Config =>
    ({
        ...config,
        cacheImage
    });

const withEnv = (overrides: typeof process.env, fn: Function): void => {
    let oldEnv: typeof process.env;

    beforeEach(() => {
        oldEnv = process.env
        process.env = { ...process.env, ...overrides }
    })

    afterEach(() => {
        process.env = oldEnv
    })

    fn()
}

const createExecWithDefaults = (overrides: Partial<CreateExecInput>) => {
    const defaultOpts = {
        config: {},
        baseDir: '',
        writeConfig: () => {},
        runDockerCompose: () => Promise.resolve(Completion.of(0)),
        runInContainer: () => Promise.resolve(Completion.of(0)),
        dockerClient: { imageExistsLocally: () => Promise.resolve(false) }
    };

    return createExec(Object.assign({}, defaultOpts, overrides));
};

describe('when config.fingerprint is outdated', () => {
    it('runs "compose build" before executing the command', async () => {
        // given
        const config = withOutdatedFingerprint(defaultConfig);
        const runDockerCompose = jest.fn(() => Promise.resolve(Completion.of(0)));
        const exec = createExecWithDefaults({
            config,
            runDockerCompose,
        });

        // when
        await exec('COMMAND');

        // then
        // @ts-ignore
        expect(runDockerCompose).toHaveBeenNthCalledWith(1,
            expect.objectContaining({
                dockerComposeArgs: ['build'],
            }),
        );
    });
});

describe('when config.fingerprint is up to date', () => {
    it('does not run "compose build" before executing the command', async () => {
        // given
        const config = withUpToDateFingerprint(defaultConfig);
        const runDockerCompose = jest.fn();
        const exec = createExecWithDefaults({
            config,
            runDockerCompose,
        });

        // when
        await exec('COMMAND');

        // then
        expect(runDockerCompose).not.toHaveBeenCalledWith(expect.objectContaining({
            dockerComposeArgs: ['build']
        }));
    });
});

describe('when executing the command', () => {
    it('updates config.fingerprint', async () => {
        // given
        const config = withOutdatedFingerprint(defaultConfig);
        const expectedFingerprint = withUpToDateFingerprint(defaultConfig).fingerprint;
        const writeConfig = jest.fn();
        const baseDir = 'BASE DIR';
        const exec = createExecWithDefaults({
            config,
            writeConfig,
            baseDir,
        });

        // when
        await exec('COMMAND');

        // then
        expect(writeConfig).toHaveBeenCalledWith(
            baseDir,
            expect.objectContaining({
                fingerprint: expectedFingerprint,
            }),
        );
    });
});

it('returns a Promise that resolves with a completion object', async () => {
    const exec = createExecWithDefaults({});
    const promise = exec('COMMAND');

    expect(promise.then).toBeDefined();
    await expect(promise).resolves.toEqual(
        expect.objectContaining({
            code: expect.any(Number),
        }),
    );
});

describe('when cache image is specified', () => {
    describe('when image _is not_ available locally', () => {
        it('tries to pull', async () => {
            const runDockerCompose = jest.fn(() => Promise.resolve(Completion.of(0)));
            const dockerClient = {
                imageExistsLocally: jest.fn()
            };
            const exec = createExecWithDefaults({
                config: withCacheImage(defaultConfig, 'image:tag'),
                runDockerCompose,
                dockerClient
            });

            dockerClient.imageExistsLocally.mockResolvedValue(false);
            await exec('COMMAND');

            expect(runDockerCompose).toHaveBeenNthCalledWith(1, expect.objectContaining({
                dockerComposeArgs: ['pull', 'dockerized'],
                rejectOnNonZeroExitCode: false
            }))
        })
    })

    describe('when image _is_ available locally', () => {
        it('does not pull', async () => {
            const runDockerCompose = jest.fn(() => Promise.resolve(Completion.of(0)));
            const dockerClient = {
                imageExistsLocally: jest.fn()
            };
            const exec = createExecWithDefaults({
                config: withCacheImage(defaultConfig, 'image:tag'),
                dockerClient,
                runDockerCompose
            });

            dockerClient.imageExistsLocally.mockResolvedValue(true);
            await exec('COMMAND');

            expect(runDockerCompose).not.toHaveBeenCalledWith(expect.objectContaining({
                dockerComposeArgs: ['pull'],
                rejectOnNonZeroExitCode: false
            }))
        })
    })

    describe('when local image was updated', () => {
        withEnv({ CI: '' }, () => {
            it('tries to push', async () => {
                const configToForceBuild = withOutdatedFingerprint(defaultConfig); // force build
                const config = withCacheImage(configToForceBuild, 'image:tag')
                const runDockerCompose = jest.fn(() => Promise.resolve(Completion.of(0)));

                const exec = createExecWithDefaults({
                    config,
                    runDockerCompose
                })

                await exec('COMMAND')

                expect(runDockerCompose).toHaveBeenCalledWith(expect.objectContaining({
                    dockerComposeArgs: ['push', 'dockerized'],
                    rejectOnNonZeroExitCode: false
                }))
            })
        })
    })

    describe('when local image was updated, but CI=true', () => {
        withEnv({ CI: 'true' }, () => {
            it('does not push', async () => {
                const configToForceBuild = withOutdatedFingerprint(defaultConfig); // force build
                const config = withCacheImage(configToForceBuild, 'image:tag')
                const runDockerCompose = jest.fn(() => Promise.resolve(Completion.of(0)));

                const exec = createExecWithDefaults({
                    config,
                    runDockerCompose
                })

                await exec('COMMAND')

                expect(runDockerCompose).not.toHaveBeenCalledWith(expect.objectContaining({
                    dockerComposeArgs: ['push'],
                }))
            })
        })
    })

    describe('when local image was _not_ updated', () => {
        it('does not push', async () => {
            const config = withUpToDateFingerprint(withCacheImage(defaultConfig, 'image:tag'))
            const runDockerCompose = jest.fn(() => Promise.resolve(Completion.of(0)));

            const exec = createExecWithDefaults({
                config,
                runDockerCompose
            })

            await exec('COMMAND')

            expect(runDockerCompose).not.toHaveBeenCalledWith(expect.objectContaining({
                dockerComposeArgs: ['push', 'dockerized'],
            }))
        })
    })
})

