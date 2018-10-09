const debug = require('debug')('dockerized:find-base-dir')
const findUp = require('dnif')

module.exports = function findBaseDir() {
  return new Promise((resolve, reject) => {
    const options = {
      name: '.dockerized',
      startPath: process.cwd()
    }
    findUp(options, (err, dir) => {
      if (err) {
        reject(new Error(err))
      } else if (dir === null) {
        reject(
          new Error(
            `could not find ${options.name} (did you run 'dockerized init'?)`
          )
        )
      } else {
        debug(`found .dockerized in ${dir}`)
        resolve(dir)
      }
    })
  })
}
