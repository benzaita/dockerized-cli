# Use with VSCode Remote Containers

VSCode Remote Containers allows you to define a development environment in Docker, just like dockerized. However, in a build server environment you are probably not running VSCode. dockerized can be configured to use the development environment defined by VSCode Remote Containers, so you can use them outside VSCode.

VSCode defines the development environment in a `.devcontainer` directory using a `Dockerfile` and possibly a `docker-compose.yml` file, very similarly to dockerized. To configure dockerized to use that environment follow these instructions:

## When the .devcontainer directory contains only a Dockerfile

Run this to initialize your dockerized project:

```shell
dockerized init --from https://github.com/benzaita/dockerized-example-vscode.git
```

## When the .devcontainer directory contains both Dockerfile and docker-compose.yml

Run this to initialize your dockerized project:

```shell
dockerized init --from https://github.com/benzaita/dockerized-example-vscode-docker-compose.git
```
