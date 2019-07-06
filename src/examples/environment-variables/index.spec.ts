import stdoutOfDockerized from '../../utils/stdout-of-dockerized'

jest.setTimeout(10000)

afterAll(() => {
  stdoutOfDockerized('clean')
})

describe('when passing environment variables to "exec"', () => {
  it('they should be defined in the container', () => {
    expect(stdoutOfDockerized(`exec FOO=foo 'env | grep FOO'`)).toMatch('FOO=foo')
  })
})
