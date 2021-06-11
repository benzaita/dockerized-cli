# Starter Kits

To start using dockerized you can either initialize an empty project using `dockerized init`, or use a “starter kit”. A starter kit is a predefined environment that you can customize.

To initialize a project using a starter kit use:

```shell
dockerized init --from <GIT REPOSITORY URL>
```

Here are a couple of starter kits which are available:

## Python

```shell
dockerized init --from https://github.com/benzaita/dockerized-example-python.git
```

## Go

```shell
dockerized init --from https://github.com/benzaita/dockerized-example-golang.git
```

## Node.js

```shell
dockerized init --from https://github.com/benzaita/dockerized-example-nodejs.git
```

## VSCode

If you are using VSCode Remote Containers, and your `.devcontainer/` is using _only_ a `Dockerfile` file (without a `docker-compose.yml` file):

```shell
dockerized init --from https://github.com/benzaita/dockerized-example-vscode.git
```

And if your `.devcontainer/` contains both `Dockerfile` and `docker-compose.yml` files:

```shell
dockerized init --from https://github.com/benzaita/dockerized-example-vscode-docker-compose.git
```

[Open an issue](https://github.com/benzaita/dockerized-cli/issues/new) to suggest more!
