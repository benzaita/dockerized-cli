# dockerized 🏗❤️

`dockerized` helps you express your build dependencies in code, and seamlessly use them - just append `dockerized exec`!

* Never again an outdated README file with all the tools you need to install to build your project.

* Never again your build dependencies managed in another repo which falls out of sync with your code.

Your build dependencies are part of your project.

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
