import fs from 'fs';

export default function writeConfig(baseDir: string, config: object): void {
    const configFile = `${baseDir}/.dockerized/config.json`;
    fs.writeFileSync(configFile, JSON.stringify(config, null, 2));
}
