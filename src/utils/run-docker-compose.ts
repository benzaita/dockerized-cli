import childProcess from 'child_process';
import path from 'path';
import createDebug from 'debug';
import Completion from './completion';

const debug = createDebug('dockerized:docker-compose');

export interface RunDockerComposeInput {
    baseDir: string;
    dockerComposeFile: string;
    dockerComposeArgs: string[];
    rejectOnNonZeroExitCode: boolean;
}

export default function runDockerCompose({
    baseDir,
    dockerComposeFile,
    dockerComposeArgs,
    rejectOnNonZeroExitCode,
}: RunDockerComposeInput): Promise<Completion> {
    const args = [
        '-f', path.resolve(baseDir, dockerComposeFile),
        '--project-name', baseDir,
        ...dockerComposeArgs
    ];

    debug(`running: docker-compose ${args.join(' ')}`);
    return new Promise((resolve, reject) => {
        const child = childProcess.spawn('docker-compose', args, {
            stdio: 'inherit',
        });

        child.on('exit', codeOrNull => {
            debug(`child process exited with code ${codeOrNull}`);
            const code = codeOrNull || 0;
            if (code !== 0 && rejectOnNonZeroExitCode) {
                reject(Completion.of(code));
            } else {
                resolve(Completion.of(code));
            }
        });
    });
}
