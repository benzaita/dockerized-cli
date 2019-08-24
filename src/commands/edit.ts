import { spawnSync } from 'child_process'
import { Command, flags } from '@oclif/command';
import findBaseDir from '../utils/find-base-dir';
import createReadConfig from '../utils/read-config';
import prettifyErrors from '../utils/prettify-errors';
import { getFilePathByIdentifier } from '../utils/get-file-path-by-identifier';

const readConfig = createReadConfig();

function execEditor(filePath: string) {
    const editor = process.env.DOCKERIZED_EDITOR || 'vi'

    const spawnResult = spawnSync(
        editor,
        [filePath],
        {
            stdio: 'inherit'
        }
      )
    
    if (spawnResult.status !== 0) {
        console.error(`the following command exited with code ${spawnResult.status}:`);
        console.error('')
        console.error(editor)
    }

      return spawnResult.status
}

export default class Edit extends Command {
    public static description = 'edit the Dockerfile or Docker Compose file'
    
    public static flags = {
        file: flags.string({
            description: 'file to edit',
            options: ['dockerfile', 'composefile'],
            default: 'dockerfile',
        }),
    }

    public async run() {
        const { args, flags } = this.parse(Edit);

        return prettifyErrors(async () => {
            const baseDir = await findBaseDir();
            const config = readConfig(baseDir);

            const filePath = getFilePathByIdentifier(flags.file, config, baseDir)
            console.error(`$DOCKERIZED_EDITOR ${filePath}`)
            return execEditor(filePath);
        })();
    }
}
