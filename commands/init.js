const fs = require('fs')

const composeFileTemplate = `
version: '2'
services:
  # Keep this name so builder can find it
  builder:
    # Use whatever image you want. Just make sure
    # it is able to run arbitrary commands, e.g.:
    #   docker run YOUR_IMAGE ls -l
    image: busybox
`

module.exports = function init(argv) {
  const config = {
    composeFile: argv.file
  }

  if (fs.existsSync('.builder')) {
    throw new Error('already initialized')
  }

  if (fs.existsSync(config.composeFile)) {
    throw new Error(`will not overwrite ${config.composeFile}. Use --file to choose a different name`)
  }

  fs.mkdirSync('.builder')
  fs.writeFileSync('.builder/config.json', JSON.stringify(config, null, 2))
  console.error('created .builder/')

  fs.writeFileSync(config.composeFile, composeFileTemplate)
  console.error(`created ${config.composeFile}`)
}
