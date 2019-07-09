dockerized 🏗❤️
================

[![oclif](https://img.shields.io/badge/cli-oclif-brightgreen.svg)](https://oclif.io)
[![Version](https://img.shields.io/npm/v/dockerized-cli.svg)](https://npmjs.org/package/dockerized-cli)
[![Downloads/week](https://img.shields.io/npm/dw/dockerized-cli.svg)](https://npmjs.org/package/dockerized-cli)
[![License](https://img.shields.io/npm/l/dockerized-cli.svg)](https://github.com/benzaita/dockerized-cli/blob/master/package.json)

`dockerized` is a tool for seamlessly executing commands in a container. It takes care of the details so you can run a command in a container as if it was running on your machine - just prepend any command with `dockerized exec` to have it run in the container.

This is especially useful for building things. For example, if your project needs Java and Maven to build, you can put these build dependencies in a Dockerfile and then just replace `mvn` with `dockerized exec mvn`. If your tests need a Postgresql database to run, add that in a Docker Compose file and just run `dockerized exec mvn test`.

That approach encourages versioning the build dependencies _alongside_ the application code.

* Never again an outdated README file with all the tools you need to install to build your project.
* Never again your build dependencies managed in another repo which falls out of sync with your code.

Your build dependencies are part of your project!

# Getting Started

Install _dockerized_:

```
npm install -g dockerized-cli
```

Run `dockerized init` to set up. It will create a Dockerfile and a Docker Compose file for you. You can tweak those to set up your build dependencies.

Then run `dockerized exec COMMAND` to build the container, start the dependencies, and execute `COMMAND` inside a container.

Contents:

<!-- toc -->
* [Getting Started](#getting-started)
* [Usage](#usage)
* [Examples](#examples)
* [Commands](#commands)
* [Advanced Usage](#advanced-usage)
<!-- tocstop -->

# Usage

<!-- usage -->
```sh-session
$ npm install -g dockerized-cli
$ dockerized COMMAND
running command...
$ dockerized (-v|--version|version)
dockerized-cli/0.4.2 darwin-x64 node-v8.15.1
$ dockerized --help [COMMAND]
USAGE
  $ dockerized COMMAND
...
```
<!-- usagestop -->

# Examples

See the `src/examples/` folder.

# Commands
<!-- commands -->
* [`dockerized clean`](#dockerized-clean)
* [`dockerized compose`](#dockerized-compose)
* [`dockerized exec [NAME=VALUE ...] COMMAND`](#dockerized-exec-namevalue--command)
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

_See code: [src/commands/clean.ts](https://github.com/benzaita/dockerized-cli/blob/v0.4.2/src/commands/clean.ts)_

## `dockerized compose`

run a docker-compose command

```
USAGE
  $ dockerized compose

EXAMPLES
  $ dockerized compose ps
  ...
```

_See code: [src/commands/compose.ts](https://github.com/benzaita/dockerized-cli/blob/v0.4.2/src/commands/compose.ts)_

## `dockerized exec [NAME=VALUE ...] COMMAND`

execute a command inside the dockerized environment

```
USAGE
  $ dockerized exec [NAME=VALUE ...] COMMAND

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

_See code: [src/commands/exec.ts](https://github.com/benzaita/dockerized-cli/blob/v0.4.2/src/commands/exec.ts)_

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
  --composeFile=composeFile  [default: .dockerized/docker-compose.dockerized.yml] Docker-Compose file to create
  --dockerFile=dockerFile    [default: .dockerized/Dockerfile.dockerized] Dockerfile to create
  --withGoCache              Includes a volume for GOPATH
  --withNestedDocker         Includes support for running Docker inside Docker
  --withYarnCache            Includes support for utilizing yarn cache

EXAMPLE
  $ dockerized init
```

_See code: [src/commands/init.ts](https://github.com/benzaita/dockerized-cli/blob/v0.4.2/src/commands/init.ts)_

## `dockerized shell`

drop into an interactive shell inside the dockerized

```
USAGE
  $ dockerized shell
```

_See code: [src/commands/shell.ts](https://github.com/benzaita/dockerized-cli/blob/v0.4.2/src/commands/shell.ts)_
<!-- commandsstop -->

# Advanced Usage

## Environment variables

The environment variables available to the dockerized command consists of:

- Environment variables defined in `.dockerized/Dockerfile.dockerized`
- Environment variables defined in `.dockerized/docker-compose.dockerized.yml`
- Environment variables passed to the `exec` command: `dockerized exec FOO=1 BAR=2 COMMAND`

## My project uses Yarn - how do I utilize its cache?

```sh
$ dockerized init --withYarnCache
```
