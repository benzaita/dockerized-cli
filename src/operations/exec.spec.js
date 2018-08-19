const execFactory = require('./exec')
const fingerprint = require('../utils/fingerprint-config')
const Completion = require('../utils/completion')

const withOutdatedFingerprint = config =>
  Object.assign({}, config, {
    fingerprint: 'FOO'
  })

const withUpToDateFingerprint = config =>
  Object.assign({}, config, {
    fingerprint: fingerprint(config)
  })

const createExec = opts => {
  const defaultOpts = {
    config: {},
    baseDir: '',
    writeConfig: () => {},
    runDockerCompose: () => Completion.of(0),
    runInContainer: () => Completion.of(0)
  }

  return execFactory(Object.assign({}, defaultOpts, opts))
}

describe('when config.fingerprint is outdated', () => {
  it('runs "compose build" before executing the command', async () => {
    // given
    const config = withOutdatedFingerprint({})
    const runDockerCompose = jest.fn(() => Completion.of(0))
    const exec = createExec({
      config,
      runDockerCompose
    })

    // when
    await exec('COMMAND')

    // then
    expect(runDockerCompose.mock.calls[0][0]).toEqual(
      expect.objectContaining({
        dockerComposeArgs: ['build']
      })
    )
  })
})

describe('when config.fingerprint is up to date', () => {
  it('does not run "compose build" before executing the command', async () => {
    // given
    const config = withUpToDateFingerprint({})
    const runDockerCompose = jest.fn()
    const exec = createExec({
      config,
      runDockerCompose
    })

    // when
    await exec('COMMAND')

    // then
    expect(runDockerCompose).not.toHaveBeenCalled()
  })
})

describe('when executing the command', () => {
  it('updates config.fingerprint', async () => {
    // given
    const config = withOutdatedFingerprint({})
    const expectedFingerprint = withUpToDateFingerprint({}).fingerprint
    const writeConfig = jest.fn()
    const baseDir = 'BASE DIR'
    const exec = createExec({
      config,
      writeConfig,
      baseDir
    })

    // when
    await exec('COMMAND')

    // then
    expect(writeConfig).toHaveBeenCalledWith(
      baseDir,
      expect.objectContaining({
        fingerprint: expectedFingerprint
      })
    )
  })
})

it('returns a Promise that resolves with a completion object', async () => {
  const exec = createExec()
  const promise = exec('COMMAND')

  expect(promise.then).toBeDefined()
  await expect(promise).resolves.toEqual(
    expect.objectContaining({
      code: expect.any(Number)
    })
  )
})
