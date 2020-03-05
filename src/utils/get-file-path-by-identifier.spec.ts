import { getFilePathByIdentifier } from "./get-file-path-by-identifier";
import { Config } from './read-config';

it('returns correct path for "dockerfile"', () => {
    expect(getFilePathByIdentifier(
        'dockerfile',
        createConfig({ dockerFile: 'Dockerfile' }),
        'base-dir'
    )).toEqual(
        'base-dir/.dockerized/Dockerfile'
    )
});

it('returns correct path for "composefile"', () => {
    expect(getFilePathByIdentifier(
        'composefile',
        createConfig({ composeFile: '.dockerized/docker-compose.yml' }),
        'base-dir'
    )).toEqual(
        'base-dir/.dockerized/docker-compose.yml'
    )
});

function createConfig(partial: Partial<Config>): Config {
    return Object.assign(
        {
            dockerFile: 'dockerFile',
            dockerFileFingerprint: 'dockerFileFingerprint',
            composeFileFingerprint: 'composeFileFingerprint',
            fingerprint: 'fingerprint',
            composeFile: 'composeFile',
            cacheImage: 'cacheImage'
        },
        partial
    );
}

