# Cache the “dockerized” Docker image

When running in CI dockerized probably runs on a fresh node where the "dockerized" image is not available yet. Therefore, it needs to build it from scratch. This can be a long process of downloading and installing build dependencies. Doing this over and over again on every fresh node is wasteful.

Let's illustrate this using the following `./dockerized/Dockerfile.dockerized` file:

```Dockerfile
FROM busybox
RUN echo "long operation"
```

## Configuring to pull the cache image

Make the following changes to your `./dockerized/docker-compose.dockerized.yml` file:

```yaml hl_lines="4 8 9"
 version: '3.2'
 services:
   dockerized:
     image: benzaita/dockerized-fixture-with_build_cache
     build:
       context: .
       dockerfile: Dockerfile.dockerized
       cache_from:
         - benzaita/dockerized-fixture-with_build_cache
     entrypoint:
       - sh
       - '-c'
```

dockerized first tries to pulls the `dockerized` image before building it so Docker can utilize it. If the image was built using the same Dockerfile, Docker will use the cache from `benzaita/dockerized-fixture-with_build_cache` instead of executing the `RUN echo "long operation"` line during build. When you run a command using `dockerized exec` you can expect the following:

```plain
Pulling dockerized ... done
Building dockerized
...
Step 2/2 : RUN echo "long operation"
 ---> Using cache
...
```

## Pushing the cache image

Having a remote cache for the image means you need to decide when to update it -- when to run `dockerized push`.

It is recommended to run `dockerized push` at the end of your CI pipeline. This ensures that (a) the pipeline successfully runs with this `dockerized` image (so you don't push a broken image) and (b) incurs a very small overhead since in most of the builds the Docker image is already up to date and Docker does not push the layers.

Another option is to let the developer run `dockerized push` after they commit a change to the `.dockerized/Dockerfile.dockerized` file. This does not require any automation, but means the developer might forget to do it, rendering the cache out of date.
