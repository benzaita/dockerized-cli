const findBaseDir = require("../utils/find-base-dir")
const readConfig = require("../utils/read-config")
const prettifyErrors = require("../utils/prettify-errors")
const execInDockerCompose = require("../utils/exec-in-docker-compose")

module.exports = {
  command: "exec",
  desc: "execute a command inside the builder",
  builder: yargs => yargs,
  handler: prettifyErrors(async function exec(argv) {
    const command = process.argv.slice(3).join(" ")
    const baseDir = await findBaseDir()
    const config = readConfig(baseDir)
    const dockerComposeFile = config.composeFile

    execInDockerCompose(command, baseDir, dockerComposeFile)
  })
}
