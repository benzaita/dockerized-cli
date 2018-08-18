const DockerCompose = require("../utils/docker-compose")

module.exports = function execInDockerCompose(
  command,
  baseDir,
  dockerComposeFile
) {
  DockerCompose.spawn({
    baseDir,
    dockerComposeFile,
    dockderComposeArgs: [
      "run",
      "--rm",
      "-v",
      `${baseDir}:${baseDir}`,
      "-w",
      process.cwd(),
      "builder",
      command
    ]
  })
}
