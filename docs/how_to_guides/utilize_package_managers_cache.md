# Utilize Package-Managers Cache

Suppose you have a build container that has Yarn installed. When you run `yarn` inside that container Yarn has to download the Yarn packages even if it already downloaded them in a previous run. To resolve this, the cache needs to be persisted between runs.

The same is true for most of the package managers - Yarn, Maven, Gradle, Pip, ...

In the next sections, you can find recipes for persisting the cache directory of each package manager.

## Yarn

Add this to your `.dockerized/docker-compose.dockerized.yml`:

```yaml hl_lines="4 6 8"
 services:
   dockerized:
     environment:
       - YARN_CACHE_FOLDER=/data/yarn-cache
     volumes:
       - 'yarn-cache:/data/yarn-cache'
 volumes:
   yarn-cache: {}
```

## Maven

Add this to your `.dockerized/docker-compose.dockerized.yml`:

```yaml hl_lines="4 6"
 services:
   dockerized:
     volumes:
       - maven-cache:/root/.m2
 volumes:
   maven-cache: {}
```

## Gradle

Add this to your `.dockerized/docker-compose.dockerized.yml`:

```yaml hl_lines="4 6"
 services:
   dockerized:
     volumes:
       - gradle-cache:/root/.gradle
 volumes:
   gradle-cache: {}
```

## Pip

Add this to your `.dockerized/docker-compose.dockerized.yml`:

```yaml hl_lines="4 6"
 services:
   dockerized:
     volumes:
       - pip-cache:/root/.cache/pip
 volumes:
   pip-cache: {}
```
