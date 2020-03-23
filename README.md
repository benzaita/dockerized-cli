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

### Why not `docker run` or `docker exec`?

Fair question! After all _dockerized_ is just a wrapper for Docker. You can definitely use `docker run` or `docker exec` but there are a few details you'd have to take care of:

**Rebuilding the Docker image:** after changing the `Dockerfile`, you need to run `docker build` before running `docker run` again. When iterating on the `Dockerfile` this can become a pain.

With _dockerized_ you just do `dockerized exec`.

**Volumes and working directory**: to allow the developer to run commands from arbitrary locations within the project, you probably want to mount the project root into the container. Manually running `docker run -v $PWD:...` one time and `docker run -v $PWD/..:...` another time, or adding some script to do this for you.

With _dockerized_ you just do `dockerized exec`.

**Running Docker Compose:** almost every project has integration tests. Running them locally usually means running Docker Compose. Now you need to run `docker-compose up` before running `docker run`. Besides being annoying, see also "Port contamination" below.

With _dockerized_ you just do `dockerized exec`.

**"Port contamination":** many people run their tests on the host, against dependencies (think PostgreSQL for example) running in containers. Since the tests need to access the PostgreSQL port, they expose this port to the host. When you are working on multiple projects these exposed ports start conflicting and you have to `docker-compose stop` one project before `docker-compose start` the other.

With _dockerized_ you just do `dockerized exec`.

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
dockerized-cli/0.8.0 darwin-x64 node-v12.16.1
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
* [`dockerized edit`](#dockerized-edit)
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

_See code: [src/commands/clean.ts](https://github.com/benzaita/dockerized-cli/blob/v0.8.0/src/commands/clean.ts)_

## `dockerized compose`

run a docker-compose command

```
USAGE
  $ dockerized compose

EXAMPLES
  $ dockerized compose ps
  ...
```

_See code: [src/commands/compose.ts](https://github.com/benzaita/dockerized-cli/blob/v0.8.0/src/commands/compose.ts)_

## `dockerized edit`

edit the Dockerfile or Docker Compose file

```
USAGE
  $ dockerized edit

OPTIONS
  --file=dockerfile|composefile  [default: dockerfile] file to edit
```

_See code: [src/commands/edit.ts](https://github.com/benzaita/dockerized-cli/blob/v0.8.0/src/commands/edit.ts)_

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

_See code: [src/commands/exec.ts](https://github.com/benzaita/dockerized-cli/blob/v0.8.0/src/commands/exec.ts)_

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

_See code: [src/commands/init.ts](https://github.com/benzaita/dockerized-cli/blob/v0.8.0/src/commands/init.ts)_

## `dockerized shell`

drop into an interactive shell inside the dockerized

```
USAGE
  $ dockerized shell
```

_See code: [src/commands/shell.ts](https://github.com/benzaita/dockerized-cli/blob/v0.8.0/src/commands/shell.ts)_
<!-- commandsstop -->

# Advanced Usage

## Environment variables

The environment variables available to the dockerized command consists of:

- Environment variables defined in `.dockerized/Dockerfile.dockerized`
- Environment variables defined in `.dockerized/docker-compose.dockerized.yml`
- Environment variables passed to the `exec` command: `dockerized exec FOO=1 BAR=2 COMMAND`

## Caching the image

`dockerized` supports caching of the builder image (the image that contains your build dependencies). If you add `image`
to the `dockerized` service of the Docker Compose file:

```shell script
dockerized edit --file=composeFile
```

```diff
 services:
   dockerized:
+    image: remote-image-uri:latest
     build:
```

`dockerized` will pull that image and use it when building your Dockerfile. The result is faster builds!

## My project uses Yarn - how do I utilize its cache?

```sh
$ dockerized init --withYarnCache
```
