import execDockerizedSync from '../../utils/exec-dockerized-sync'

jest.setTimeout(10000)

afterAll(() => {
  execDockerizedSync('clean')
})

describe('when passing environment variables to "exec"', () => {
  it('they should be defined in the container', () => {
    expect(execDockerizedSync('exec', ['FOO=foo', 'env | grep FOO']).stdout).toMatch('FOO=foo')
  })
})
