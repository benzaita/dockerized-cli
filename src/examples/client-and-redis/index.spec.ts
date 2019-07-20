import execDockerizedSync from '../../utils/exec-dockerized-sync'

jest.setTimeout(10000)

afterAll(() => {
  execDockerizedSync('clean')
})

describe('a service is defined in the Docker Compose file', () => {
  it('it is available', () => {
    expect(execDockerizedSync('exec', ['./client']).stdout).toMatch(/\+PONG/)
  })
})
