const md5 = require('md5')

module.exports = config => {
  const configWithoutFingerprint = Object.assign({}, config, {
    fingerprint: ''
  })

  return md5(JSON.stringify(configWithoutFingerprint))
}
