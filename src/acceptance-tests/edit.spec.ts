import * as fs from 'fs'
import execDockerizedSync from "../utils/exec-dockerized-sync";
import deltree from "deltree"
import { EOL } from 'os';

let workdir: string

beforeEach(() => {
    workdir = fs.mkdtempSync('dockerized-test-')
})

afterEach(async () => {
    await deltree(workdir)
})

describe('when DOCKERIZED_EDITOR is set', () => {
    beforeEach(() => {
        execDockerizedSync('init', [], { cwd: workdir })
    })

    it('should propagate exit code of DOCKERIZED_EDITOR', () => {
        const { stdout, stderr, status } = execDockerizedSync('edit', [], {
            cwd: workdir,
            env: { DOCKERIZED_EDITOR: 'false' }
        })
        expect(stderr.split(EOL)[0]).toMatch(/\$DOCKERIZED_EDITOR .*\/\.dockerized\/Dockerfile\.dockerized/)
        expect(stderr.split(EOL).slice(1)).toEqual([
            'the following command exited with code 1:',
            '',
            'false',
            ''
        ])
        expect(stdout).toEqual('')
        expect(status).toBe(1)
    })
})
