import createExec, { CreateExecInput } from './exec';
import fingerprint from '../utils/fingerprint-config';
import Completion from '../utils/completion';
import { Config } from '../utils/read-config';

const defaultConfig: Config = {
    composeFile: '',
    composeFileFingerprint: '',
    dockerFileFingerprint: '',
    fingerprint: '',
};

const withOutdatedFingerprint = (config: Config): Config =>
    Object.assign({}, config, {
        fingerprint: 'FOO',
    });

const withUpToDateFingerprint = (config: Config): Config =>
    Object.assign({}, config, {
        fingerprint: fingerprint(config),
    });

const createExecWithDefaults = (overrides: Partial<CreateExecInput>) => {
    const defaultOpts = {
        config: {},
        baseDir: '',
        writeConfig: () => {},
        runDockerCompose: () => Promise.resolve(Completion.of(0)),
        runInContainer: () => Promise.resolve(Completion.of(0)),
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
        expect(runDockerCompose.mock.calls[0][0]).toEqual(
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
        expect(runDockerCompose).not.toHaveBeenCalled();
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
