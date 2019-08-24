import createDebug from 'debug';

const debug = createDebug('dockerized');

export default function prettifyErrors(fn: Function) {
    return async function() {
        try {
            const code = await fn();
            process.exit(code)
        } catch (e) {
            debug(e);
            console.error(e.message);
            process.exit(1);
        }
    };
}
