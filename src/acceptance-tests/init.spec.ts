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

describe('when not initialized yet', () => {
    it('should initialize', () => {
        const { stdout, stderr, status } = execDockerizedSync('init', [], { cwd: workdir })
        expect(status).toBe(0)
        expect(stdout).toEqual('')
        expect(stderr.split(EOL)).toEqual([
            'created .dockerized/docker-compose.dockerized.yml',
            'created .dockerized/Dockerfile.dockerized',
            'hint: edit .dockerized/Dockerfile.dockerized to set up your container',    
            ''
        ])
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