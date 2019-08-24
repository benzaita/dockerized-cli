import { join } from 'path';
import { Config } from './read-config';

// TODO test this
export function getFilePathByIdentifier(fileIdentifier: string | undefined, config: Config, baseDir: string): string {
    if (fileIdentifier === 'dockerfile') {
        return join(baseDir, '.dockerized', config.dockerFile);
    }
    else if (fileIdentifier === 'composefile') {
        return join(baseDir, config.composeFile);
    }
    else {
        throw new Error(`Internal error (the "file" flag has an unexpected value of ${fileIdentifier})`);
    }
}
