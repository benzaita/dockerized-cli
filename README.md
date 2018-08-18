# builder 🏗❤️

`builder` helps you express your build dependencies in code, and seamlessly use them - just append `builder exec`!

* Never again an outdated README file with all the tools you need to install to build your project.

* Never again your build dependencies managed in another repo which falls out of sync with your code.

Your build dependencies are part of your project.

## Getting Started

```sh
$ builder init
created .builder/docker-compose.builder.yml
created .builder/Dockerfile.builder

$ cat .builder/Dockerfile.builder
FROM busybox
# install your build dependencies here

$ builder exec build-my-project
```

## Examples

See the `examples/` folder.

## Advanced Usage

### Environment variables

The environment variables available to the dockerized command consists of:

- Environment variables defined in `.builder/Dockerfile.builder`
- Environment variables defined in `.builder/docker-compose.builder.yml`
- Environment variables passed to the `exec` command: `builder exec FOO=1 BAR=2 COMMAND`

### My project uses Yarn - how do I utilize its cache?

```sh
$ builder init --withYarnCache
```
