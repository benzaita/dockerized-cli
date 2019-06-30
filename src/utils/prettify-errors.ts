import createDebug from 'debug';

const debug = createDebug('dockerized');

export default function prettifyErrors(fn: Function) {
    return async function() {
        try {
            await fn();
        } catch (e) {
            debug(e);
            console.error(e.message);
            process.exit(1);
        }
    };
}
