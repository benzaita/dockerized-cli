# How "dockerized exec" works

dockerized is a thin wrapper around Docker Compose. Every dockerized project contains a `.dockerized/` directory that contains a `docker-compose.dockerized.yml` at minimum. That file essentially describes the development environment. It contains at least one “service” called “dockerized”.

When you run `dockerized exec COMMAND` (for example, `dockerized exec make build`), dockerized runs `docker-compose ... run dockerized COMMAND`. To make it feel as if you are executing the command in the current directory (only in an environment that has all the tools that command needs), dockerized bind-mounts the project directory and sets the working directory accordingly. To see the exact arguments it passes set the log level to INFO:

```shell
> dockerized --loglevel=INFO exec ls -l
INFO:dockerized.core.commands.dockercomposecommand:Configuration file (/Users/benzaita/dev/sandbox/.dockerized/config.yml) does not exist. Using defaults.
INFO:dockerized.core.project:/Users/benzaita/dev/sandbox is prepared
INFO:dockerized.adapters.dockercompose:Running: [
    'docker-compose',
    '-f', '/Users/benzaita/dev/sandbox/.dockerized/docker-compose.dockerized.yml',
    '--project-name', '/Users/benzaita/dev/sandbox',
    'run',
        '--rm',
        '--service-ports',
        '-v', '/Users/benzaita/dev/sandbox:/Users/benzaita/dev/sandbox',
        '-w', '/Users/benzaita/dev/sandbox',
        'dockerized',
            'ls -l'
]
```

Note that every time you run a command, dockerized spawns a new "one-off" container that is removed when the command is completed.
