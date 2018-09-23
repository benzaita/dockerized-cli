# cenv 🏗❤️

`cenv` helps you express your build dependencies in code, and seamlessly use them - just append `cenv exec`!

* Never again an outdated README file with all the tools you need to install to build your project.

* Never again your build dependencies managed in another repo which falls out of sync with your code.

Your build dependencies are part of your project.

## Getting Started

```sh
$ npm install -g cenv
```

```sh
$ cenv init
created .cenv/docker-compose.cenv.yml
created .cenv/Dockerfile.cenv

$ cat .cenv/Dockerfile.cenv
FROM busybox
# install your build dependencies here

$ cenv exec build-my-project
```

## Examples

See the `examples/` folder.

## Advanced Usage

### Environment variables

The environment variables available to the dockerized command consists of:

- Environment variables defined in `.cenv/Dockerfile.cenv`
- Environment variables defined in `.cenv/docker-compose.cenv.yml`
- Environment variables passed to the `exec` command: `cenv exec FOO=1 BAR=2 COMMAND`

### My project uses Yarn - how do I utilize its cache?

```sh
$ cenv init --withYarnCache
```
