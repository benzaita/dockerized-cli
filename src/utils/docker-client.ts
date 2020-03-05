import {exec} from 'child_process'
import createDebug from 'debug';

const debug = createDebug('dockerized:docker-client');

export interface DockerClient {
    imageExistsLocally(image: string): Promise<boolean>;
}

export class DefaultDockerClient implements DockerClient {
    public imageExistsLocally(image: string): Promise<boolean> {
        const stdoutToResult = (stdout: string): boolean => stdout.length > 0
        return new Promise<boolean>(((resolve, reject) => {
            const cmd = `docker images -q '${image}'`;
            debug('running', cmd)
            exec(cmd, (err, stdout) => {
                if (err) {
                    reject(err)
                } else {
                    resolve(stdoutToResult(stdout))
                }
            })
        }));
    }
}
