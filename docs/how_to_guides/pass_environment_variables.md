# Pass Environment Variables

When running `dockerized exec COMMAND`, there are two ways to pass environment variables to `COMMAND`.

## In the Command Line

The easiest way is to prepend the `COMMAND` with them:

```shell
dockerized exec FOO=1 BAR=2 COMMAND
```

For example
```shell
> dockerized exec FOO=1 BAR=2 env
...
FOO=1
BAR=2
```

## Using Docker-Compose

You can define environment variables in the `.dockerized/docker-compose.dockerized.yml` file.

This is useful if you keep passing the same variables over and over, or if you don't want to have them present in the command line (for example because it is logged).

Here is an example:

```yaml hl_lines="10-12"
 version: '2'
 services:
   dockerized:
     build:
       context: .
       dockerfile: Dockerfile.dockerized
     entrypoint:
       - sh
       - '-c'
     environment:
       - FOO=1  # specify a value
       - SECRET # pass the variable from the host environment
```
