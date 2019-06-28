import runDockerCompose from './run-docker-compose';
import Completion from '../utils/completion';

export interface RunInContainerInput {
    command: string;
    baseDir: string;
    dockerComposeFile: string;
    rejectOnNonZeroExitCode: boolean;
}

export default ({
    command,
    baseDir,
    dockerComposeFile,
    rejectOnNonZeroExitCode,
}: RunInContainerInput): Promise<Completion> =>
    runDockerCompose({
        baseDir,
        dockerComposeFile,
        rejectOnNonZeroExitCode,
        dockerComposeArgs: ['run', '--rm', '-v', `${baseDir}:${baseDir}`, '-w', process.cwd(), 'dockerized', command],
    });
