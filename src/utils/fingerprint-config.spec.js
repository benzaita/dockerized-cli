const fingerprintConfig = require('./fingerprint-config')

describe('when the config changes', () => {
  it('changes the fingerprint', () => {
    expect(fingerprintConfig({ foo: 1 })).not.toEqual(
      fingerprintConfig({ foo: 2 })
    )
  })
})
