# Quick Start

Welcome! dockerized is a CLI tool for creating and using containerized development environments using Docker. In this tutorial you will learn:

- How to install dockerized
- How to define a development environment
- How to run commands in the containerized development environment

Let’s get started!

## Installing dockerized

dockerized is written in Python and available via pip:

```shell
pip install dockerized
```

You can verify the installation by running `dockerized version`.

## Initializing a project

The first step we need to take is to initialize a new workspace, or project:

```shell
> dockerized init
created
```

This creates a `.dockerized/` directory in the current directory. Let’s explore it:

```shell
> ls .dockerized/
Dockerfile.dockerized
docker-compose.dockerized.yml
```

These two files define the development environment -- the `Dockerfile` defines which tools are required (e.g. python, git, jq, make) and the `docker-compose` file defines which services it consists of. Currently our environment does not require any tools:

```shell
> cat .dockerized/Dockerfile.dockerized
FROM busybox
# Add your build dependencies here
```

And contains only a single service, “dockerized”, where our commands will run:

```shell
> cat .dockerized/docker-compose.dockerized.yml
version: '3.2'
services:
  dockerized:
    build:
      context: .
      dockerfile: Dockerfile.dockerized
    entrypoint:
      - sh
      - '-c'
```

## Defining the development environment

Let’s assume our project requires Node.js 14 and jq. Edit the `.dockerized/Dockerfile.dockerized` file and set its contents to:

```Dockerfile
FROM node:14
RUN apt-get update \
 && apt-get install -y jq
```

Run this to verify we have both Node.js and jq:

```shell
> dockerized exec jq
jq - commandline JSON processor [version 1.5-1-a5b5cbe]
--snip--
> dockerized exec node --version
v14.17.0
```

## Running commands inside the development environment

Let’s run something inside the containerized development environment now:

```shell
> echo 'console.log("Hello world!")' > main.js
> dockerized exec node main.js
Hello world!
```

To pass environment variables to the container, use this:

```shell
> echo 'console.log("Hello " + process.env["USER"])' > main.js
> dockerized exec USER=Alice node main.js
Hello Alice
```

See also the [Pass environment variables](../how_to_guides/pass_environment_variables.md) how-to guide.
