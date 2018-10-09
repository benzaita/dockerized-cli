const debug = require('debug')('dockerized')

module.exports = fn => async argv => {
  try {
    await fn(argv)
  } catch (e) {
    debug(e)
    console.error(e.message)
    process.exit(1)
  }
}
