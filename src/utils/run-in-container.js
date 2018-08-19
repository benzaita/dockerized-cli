const runDockerCompose = require('./run-docker-compose')

module.exports = ({
  command,
  baseDir,
  dockerComposeFile,
  rejectOnNonZeroExitCode
}) =>
  runDockerCompose({
    baseDir,
    dockerComposeFile,
    rejectOnNonZeroExitCode,
    dockerComposeArgs: [
      'run',
      '--rm',
      '-v',
      `${baseDir}:${baseDir}`,
      '-w',
      process.cwd(),
      'builder',
      command
    ]
  })
