dockerized 🏗❤️
================

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
pip install dockerized
```

Run `dockerized init` to set up. It will create a Dockerfile and a Docker Compose file for you. You can tweak those to set up your build dependencies.

Then run `dockerized exec COMMAND` to build the container, start the dependencies, and execute `COMMAND` inside a container.

