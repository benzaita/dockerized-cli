import createDebug from 'debug';

const debug = createDebug('dockerized');

export default function prettifyErrors(fn: Function) {
    return async function(argv: string[]) {
        try {
            await fn(argv);
        } catch (e) {
            debug(e);
            console.error(e.message);
            process.exit(1);
        }
    };
}
