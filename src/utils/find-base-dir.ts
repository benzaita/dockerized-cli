import createDebug from 'debug';
// @ts-ignore
import findUp from 'dnif';

const debug = createDebug('dockerized:find-base-dir');

export default function findBaseDir(): Promise<string> {
    return new Promise((resolve, reject) => {
        const options = {
            name: '.dockerized',
            startPath: process.cwd(),
        };
        findUp(options, (err: any, dir: string) => {
            if (err) {
                reject(new Error(err));
            } else if (dir === null) {
                reject(new Error(`could not find ${options.name} (did you run 'dockerized init'?)`));
            } else {
                debug(`found .dockerized in ${dir}`);
                resolve(dir);
            }
        });
    });
}
