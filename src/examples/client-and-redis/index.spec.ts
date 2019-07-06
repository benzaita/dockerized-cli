import stdoutOfDockerized from '../../utils/stdout-of-dockerized'

jest.setTimeout(10000)

afterAll(() => {
  stdoutOfDockerized('clean')
})

describe('a service is defined in the Docker Compose file', () => {
  it('it is available', () => {
    expect(stdoutOfDockerized(`exec ./client`)).toMatch(/\+PONG/)
  })
})
