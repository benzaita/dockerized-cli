import runDockerCompose from "./run-docker-compose";
import childProcess from 'child_process';

jest.mock('child_process', () => ({
    spawn: jest.fn(() => {
        const childObjectMock = {
            on: jest.fn()
        }

        return childObjectMock
    })
}))

it('sets the Docker Compose project name to the base dir', () => {
    const baseDir = 'BASE DIR';
    const dockerComposeFile = 'DOCKER COMPOSE FILE';
    const dockerComposeArgs = ['ARG1', 'ARG2'];
    const rejectOnNonZeroExitCode = true;

    runDockerCompose({ baseDir, dockerComposeFile, dockerComposeArgs, rejectOnNonZeroExitCode })

    expect(childProcess.spawn).toHaveBeenCalledWith(
        'docker-compose',
        expect.arrayContaining(['--project-name', baseDir]),
        expect.any(Object)
    )
})
