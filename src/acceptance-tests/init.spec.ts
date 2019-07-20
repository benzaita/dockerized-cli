import * as fs from 'fs'
import stdoutOfDockerized from "../utils/stdout-of-dockerized";
import deltree from "deltree"

describe('when not initialized yet', () => {
    let workdir: string

    beforeEach(() => {
        workdir = fs.mkdtempSync('dockerized-test-')
    })

    afterEach(async () => {
        await deltree(workdir)
    })

    it('should initialize', () => {
        const stdout = stdoutOfDockerized('init', { cwd: workdir })
        expect(stdout).toEqual('')
    })
})