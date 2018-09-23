const md5 = require('md5')
const yaml = require('js-yaml')
const readConfigFactory = require('./read-config')

const jsonToYaml = yaml.safeDump

const createReadConfig = ({ mockFilesystem }) => {
  const filesystem = Object.assign({}, mockFilesystem)
  const readFile = path => {
    if (filesystem[path] === undefined)
      throw new Error(`file not found: ${path}`)
    return filesystem[path]
  }
  return readConfigFactory({ readFile })
}

it('does not fail when composeFile is undefined', () => {
  const readConfig = createReadConfig({
    mockFilesystem: {
      'base-dir/.cenv/config.json': '{}'
    }
  })

  expect(() => readConfig('base-dir')).not.toThrow()
})

it('sets composeFileFingerprint to the fingerprint of the content of the docker-compose file', () => {
  // given
  const configFileContent = JSON.stringify({
    composeFile: '.cenv/compose-file.yml'
  })
  const readConfig = createReadConfig({
    mockFilesystem: {
      'base-dir/.cenv/config.json': configFileContent,
      'base-dir/.cenv/compose-file.yml': 'compose-file-content'
    }
  })

  // when
  const config = readConfig('base-dir')

  // then
  expect(config.composeFileFingerprint).toEqual(md5('compose-file-content'))
})

it('sets dockerFileFingerprint to the fingerprint of the content of the docker file', () => {
  // given
  const configFileContent = JSON.stringify({
    composeFile: '.cenv/compose-file.yml'
  })
  const readConfig = createReadConfig({
    mockFilesystem: {
      'base-dir/.cenv/config.json': configFileContent,
      'base-dir/.cenv/compose-file.yml': jsonToYaml({
        services: { cenv: { build: { dockerfile: 'Dockerfile' } } }
      }),
      'base-dir/.cenv/Dockerfile': 'docker-file-content'
    }
  })

  // when
  const config = readConfig('base-dir')

  // then
  expect(config.dockerFileFingerprint).toEqual(md5('docker-file-content'))
})
