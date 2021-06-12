dockerized 🏗❤️
================

Easily Docker-ize your build/development environment and seamlessly run commands inside it.

_dockerized_ is a tool for seamlessly executing commands in a container. It takes care of the details so you can run a command in a container as if it was running on your machine - just prepend any command with `dockerized exec` to have it run in the container.

# Documentation

See https://benzaita.github.io/dockerized-cli/index.html

# Getting Started

Install _dockerized_:
```shell
$ pip install dockerized
```

Initialize your environment:
```shell
$ dockerized init
$ echo FROM python:3.9 > .dockerized/Dockerfile.dockerized
```

or use an example:
```shell
$ dockerized init --from https://github.com/benzaita/dockerized-example-python.git
```

Then run a command inside that environment:
```shell
$ dockerized exec python --version
...
Python 3.9.0
```

Or drop into an interactive shell inside the environment:
```shell
$ dockerized shell
# python --version
Python 3.9.0
```
