const debug = require("debug")("builder:find-base-dir")
const findUp = require("dnif")

module.exports = function findBaseDir() {
  return new Promise((resolve, reject) => {

    const options = {
      name: ".builder",
      startPath: process.cwd()
    }
    findUp(
      options,
      (err, dir) => {
        if (err) {
          reject(new Error(err))
        }
        else if (dir === null) {
          reject(new Error(`could not find ${options.name} (did you run 'builder init'?)`))
        }
        else {
          debug(`found .builder in ${dir}`)
          resolve(dir)
        }
      }
    )
  })
}
