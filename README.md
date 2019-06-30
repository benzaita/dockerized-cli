dockerized 🏗❤️
================

[![oclif](https://img.shields.io/badge/cli-oclif-brightgreen.svg)](https://oclif.io)
[![Version](https://img.shields.io/npm/v/dockerized.svg)](https://npmjs.org/package/dockerized)
[![Downloads/week](https://img.shields.io/npm/dw/dockerized.svg)](https://npmjs.org/package/dockerized)
[![License](https://img.shields.io/npm/l/dockerized.svg)](https://github.com/benzaita/dockerized/blob/master/package.json)

`dockerized` helps you express your build dependencies in code, and seamlessly use them - just append `dockerized exec`!

* Never again an outdated README file with all the tools you need to install to build your project.

* Never again your build dependencies managed in another repo which falls out of sync with your code.

Your build dependencies are part of your project.

<!-- toc -->
* [install your build dependencies here](#install-your-build-dependencies-here)
* [Commands](#commands)
<!-- tocstop -->

## Usage

<!-- usage -->
```sh-session
$ npm install -g dockerized
$ dockerized COMMAND
running command...
$ dockerized (-v|--version|version)
dockerized/0.3.0 darwin-x64 node-v8.15.1
$ dockerized --help [COMMAND]
USAGE
  $ dockerized COMMAND
...
```
<!-- usagestop -->

## Getting Started

```sh
$ npm install -g dockerized
```

```sh
$ dockerized init
created .dockerized/docker-compose.dockerized.yml
created .dockerized/Dockerfile.dockerized

$ cat .dockerized/Dockerfile.dockerized
FROM busybox
# install your build dependencies here

$ dockerized exec build-my-project
```

## Examples

See the `examples/` folder.

# Commands
<!-- commands -->
* [`dockerized clean`](#dockerized-clean)
* [`dockerized compose`](#dockerized-compose)
* [`dockerized $ dockerized exec COMMAND`](#dockerized--dockerized-exec-command)
* [`dockerized help [COMMAND]`](#dockerized-help-command)
* [`dockerized init`](#dockerized-init)
* [`dockerized shell`](#dockerized-shell)

## `dockerized clean`

removes the container

```
USAGE
  $ dockerized clean

EXAMPLE
  $ dockerized clean
```

_See code: [src/commands/clean.ts](https://github.com/benzaita/dockerized/blob/v0.3.0/src/commands/clean.ts)_

## `dockerized compose`

run a docker-compose command

```
USAGE
  $ dockerized compose

EXAMPLES
  $ dockerized compose ps
  ...
```

_See code: [src/commands/compose.ts](https://github.com/benzaita/dockerized/blob/v0.3.0/src/commands/compose.ts)_

## `dockerized $ dockerized exec COMMAND`

execute a command inside the dockerized environment

```
USAGE
  $ dockerized $ dockerized exec COMMAND

DESCRIPTION
  Environment variables:
     To provide environment variables, either add them in the docker-compose
     file or pass them in the command line:

     dockerized exec FOO=1 BAR=2 COMMAND

EXAMPLES
  $ dockerized exec ls -l
  $ dockerized exec make build
  $ dockerized exec mvn
```

_See code: [src/commands/exec.ts](https://github.com/benzaita/dockerized/blob/v0.3.0/src/commands/exec.ts)_

## `dockerized help [COMMAND]`

display help for dockerized

```
USAGE
  $ dockerized help [COMMAND]

ARGUMENTS
  COMMAND  command to show help for

OPTIONS
  --all  see all commands in CLI
```

_See code: [@oclif/plugin-help](https://github.com/oclif/plugin-help/blob/v2.2.0/src/commands/help.ts)_

## `dockerized init`

initialize dockerized in this directory (see also: init --help)

```
USAGE
  $ dockerized init

OPTIONS
  -C, --composeFile=composeFile  [default: .dockerized/docker-compose.dockerized.yml] Docker-Compose file to create
  -D, --dockerFile=dockerFile    [default: .dockerized/Dockerfile.dockerized] Dockerfile to create
  -d, --[no-]withNestedDocker    Includes support for running Docker inside Docker
  -y, --[no-]withYarnCache       Includes support for utilizing yarn cache

EXAMPLE
  $ dockerized init
```

_See code: [src/commands/init.ts](https://github.com/benzaita/dockerized/blob/v0.3.0/src/commands/init.ts)_

## `dockerized shell`

drop into an interactive shell inside the dockerized

```
USAGE
  $ dockerized shell
```

_See code: [src/commands/shell.ts](https://github.com/benzaita/dockerized/blob/v0.3.0/src/commands/shell.ts)_
<!-- commandsstop -->

## Advanced Usage

### Environment variables

The environment variables available to the dockerized command consists of:

- Environment variables defined in `.dockerized/Dockerfile.dockerized`
- Environment variables defined in `.dockerized/docker-compose.dockerized.yml`
- Environment variables passed to the `exec` command: `dockerized exec FOO=1 BAR=2 COMMAND`

### My project uses Yarn - how do I utilize its cache?

```sh
$ dockerized init --withYarnCache
```
