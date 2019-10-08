import * as fs from 'fs'
import execDockerizedSync from "../utils/exec-dockerized-sync";
import deltree from "deltree"
import { EOL } from 'os';
import { join } from 'path';

let workdir: string

beforeEach(() => {
    workdir = fs.mkdtempSync('dockerized-test-')
})

afterEach(async () => {
    await deltree(workdir)
})

describe('when not initialized yet', () => {
    it('should return expected output', () => {
        const { stdout, stderr, status } = execDockerizedSync('init', [], { cwd: workdir })
        expect(status).toBe(0)
        expect(stdout).toEqual('')
        expect(stderr.split(EOL)).toEqual([
            'created .dockerized/docker-compose.dockerized.yml',
            'created .dockerized/Dockerfile.dockerized',
            '',
            'run the following to set up your container',
            '',
            '    dockerized edit                     # to edit the Dockerfile',
            '    dockerized edit --file=composefile  # to edit the Docker Compose file',
            ''
        ])
    })

    it('should create a README file', () => {
        execDockerizedSync('init', [], { cwd: workdir })
        const readmeFilePath = join(workdir, '.dockerized', 'README.md')
        expect(fs.existsSync(readmeFilePath)).toBeTruthy()
    })
})

describe('when already initialized', () => {
    beforeEach(() => {
        execDockerizedSync('init', [], { cwd: workdir })
    })

    it('should fail', () => {
        const { stdout, stderr, status } = execDockerizedSync('init', [], { cwd: workdir })
        expect(status).toBe(1)
        expect(stdout).toEqual('')
        expect(stderr.split(EOL)).toEqual([
            'already initialized',    
            ''
        ])
    })
})