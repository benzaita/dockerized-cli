import md5 from 'md5';

export default (config: object) => {
    const configWithoutFingerprint = Object.assign({}, config, {
        fingerprint: '',
    });

    return md5(JSON.stringify(configWithoutFingerprint));
};
