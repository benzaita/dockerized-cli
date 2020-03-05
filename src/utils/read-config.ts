import createDebug from 'debug';
import fs from 'fs';
import path from 'path';
import md5 from 'md5';
import R from 'ramda';
import yaml from 'js-yaml';

const debug = createDebug('dockerized:read-config');

export interface CreateReadConfigInput {
    readFileSync(path: string): Buffer;
}

const DEFAULT_READ_CONFIG_DEPS: CreateReadConfigInput = {
    readFileSync: fs.readFileSync,
};

export interface Config {
    dockerFileFingerprint: string;
    composeFileFingerprint: string;
    fingerprint: string;
    composeFile: string;
    dockerFile: string;
    cacheImage: string;
}

export default function createReadConfig(deps: CreateReadConfigInput = DEFAULT_READ_CONFIG_DEPS) {
    return (baseDir: string): Config => {
        const md5Safe = (message: string) => (message === undefined ? undefined : md5(String(message)));

        const configFilePath = path.join(baseDir, '.dockerized', 'config.json');
        debug('reading file', configFilePath);
        const config = JSON.parse(String(deps.readFileSync(configFilePath)));

        if (config.composeFile) {
            const composeFilePath = path.join(baseDir, config.composeFile);
            debug('reading file', composeFilePath);
            const composeFileString = deps.readFileSync(composeFilePath);
            config.composeFileFingerprint = md5Safe(String(composeFileString));

            const composeFileJson = yaml.safeLoad(String(composeFileString));
            const dockerFilePath = R.path<string>(['services', 'dockerized', 'build', 'dockerfile'], composeFileJson);
            const cacheImage = R.path<string>(['services', 'dockerized', 'image'], composeFileJson);

            config.dockerFile = dockerFilePath
            config.cacheImage = cacheImage

            const dockerFileString =
                dockerFilePath === undefined
                    ? ''
                    : deps.readFileSync(path.join(baseDir, '.dockerized', dockerFilePath));
            config.dockerFileFingerprint = md5Safe(String(dockerFileString));
        }
        return config;
    };
}
