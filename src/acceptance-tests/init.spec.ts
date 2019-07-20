import * as fs from 'fs'
import execDockerizedSync from "../utils/exec-dockerized-sync";
import deltree from "deltree"
import { EOL } from 'os';

describe('when not initialized yet', () => {
    let workdir: string

    beforeEach(() => {
        workdir = fs.mkdtempSync('dockerized-test-')
    })

    afterEach(async () => {
        await deltree(workdir)
    })

    it('should initialize', () => {
        const { stdout, stderr, status } = execDockerizedSync('init', [], { cwd: workdir })
        expect(stdout).toEqual('')
        expect(stderr.split(EOL)).toEqual([
            'created .dockerized/docker-compose.dockerized.yml',
            'created .dockerized/Dockerfile.dockerized',
            'hint: edit .dockerized/Dockerfile.dockerized to set up your container',    
            ''
        ])
        expect(status).toBe(0)
    })
})