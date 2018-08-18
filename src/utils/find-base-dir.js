const debug = require("debug")("builder:find-base-dir")
const findUp = require("dnif")

module.exports = function findBaseDir() {
  return new Promise((resolve, reject) => {
    findUp(
      {
        name: ".builder",
        startPath: process.cwd()
      },
      (err, dir) => {
        if (err) {
          reject(new Error(err))
        }
        debug(`found .builder in ${dir}`)
        resolve(dir)
      }
    )
  })
}
