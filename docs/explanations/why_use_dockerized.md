# Why use dockerized

dockerized is a command-line tool that lets you seamlessly execute commands in a container. You can just prepend any command with `dockerized exec` to have it run inside your container. It's especially helpful for keeping your build dependencies in a Dockerfile. Think of it as `env` but for Docker.

It supports [caching of the Docker image](../how_to_guides/cache_the_dockerized_docker_image.md) and even [VSCode Remote Containers](../how_to_guides/use_with_vscode_remote_containers.md)!

## Quick Glance

In a nutshell, instead of running a command like this (relying on the user to use the correct version of Node.js and Yarn):

```shell
yarn install
```

you just pass it to dockerized:

```shell
dockerized exec yarn install
```

dockerized will run that command in a container with the correct build tools.

## Why you should keep your build dependencies in a Dockerfile

**Easy onboarding** - when a new team member joins you want them to be able to contribute as fast as possible. You _don't_ want them to spend hours/days trying to follow an outdated README file, installing build tools, and setting up their machine. Ideally, they should be able to jump in with a minimal amount of preparation.

**Consistency** - Works on My Machine (tm) but breaks on the CI/CD pipeline? Your local development environment cannot be identical to the CI/CD environment, but it should be as close as possible. If both environments use the same Dockerfile to run the build, you minimize the gap between the two.

**Conflicting dependencies** - one project requires Java 8 and the other Java 10? Does one project require Node 10 and the other Node 12? Python? True, there is `JAVA_HOME` and `nvm` and whatever for Python, but try forgetting to set `JAVA_HOME` when switching a directory only to find fifteen minutes later that you are not crazy, just forgetful. And while `avn` can automatically switch Node versions when you `cd` to another directory, it is yet another tool the developer needs to install. Worse, if they don't - the risk using the wrong Node version without even knowing.

## What I've seen people usually do (and have done by myself)

I've seen projects that rely on verbal communication and "folk tales" to have a common understanding of what the build-environment is. That should be obvious why it's bad.

I've seen projects that use a README to document what the bulid-environment is. That usually ends up with an outdated README file that nobody really follows.

I've seen projects that have a huge Dockerfile that contains all the build dependencies for all the projects of the team because "they all run in Jenkins eventually".

I've seen projects that have a proper Dockerfile with the build dependencies, but in a different repository. That's better, but it is hard to coordinate changes between the two repos (albeit, to be fair, these do not often happen).

And I've seen projects that have a proper Dockerfile with the build dependencies, in the same repo! However, these usually also require some "wrapper" script to pass all the flags to Docker - the volumes to map, the environment variables, the network mode, the working directory, etc. Why is that bad? For once, you need to re-write this wrapper for every repository. Secondly, these wrapper scripts tend to hide the CLIs of the tools they are running - instead of running `mvn -DskipTests package` you need to run `make package`. And when things break, and you need an interactive shell to figure out what went wrong, I usually resorted to `docker run --entrypoint /bin/sh ....` (or `make shell` if I was not lazy).

## What do you get with dockerized?

With dockerized you can just do `dockerized exec mvn -DskipTests package`, or `dockerized exec COMMAND` with whatever `COMMAND` you need. Need an interactive shell inside the container? Just run `dockerized shell`. dockerized takes care of building the container when necessary, mapping volumes, setting the working directory, and more. It does not, however, hide the interface of the tool you are trying to run.
