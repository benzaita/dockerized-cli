const debug = require('debug')('cenv:find-base-dir')
const findUp = require('dnif')

module.exports = function findBaseDir() {
  return new Promise((resolve, reject) => {
    const options = {
      name: '.cenv',
      startPath: process.cwd()
    }
    findUp(options, (err, dir) => {
      if (err) {
        reject(new Error(err))
      } else if (dir === null) {
        reject(
          new Error(`could not find ${options.name} (did you run 'cenv init'?)`)
        )
      } else {
        debug(`found .cenv in ${dir}`)
        resolve(dir)
      }
    })
  })
}
