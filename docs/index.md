# dockerized

Containerized development environments using Docker.

## Features

- **Toolset as Code** - Declare which build and/or development tools are needed in code, rather than in a README file.
Your CI can use exactly the same toolset as your developers.
- **Easy onboarding** - Bootstrapping a development environment is as easy as running `dockerized shell`.
- **No more "Works on my machine"** - No more "Works on my machine" because everyone in the team is using exactly the same toolset.
- **Consistency with CI** - Your CI can use exactly the same toolset as your developers.
- **Isolated environments** - No need for `nvm`, `virtualenv`, `SDKMAN`, and such. Each development environment is isolated.
- **Simple** - You no longer need to maintain messy `docker run` commands yourself.
- **Seamless** - Just prepend any command with `dockerized exec`.
- **Visual Studio Code** - "dockerized" complements VS Code and can use the [Remote Containers](https://code.visualstudio.com/docs/remote/containers) you already configured.
- **Opt in** - You can use the "dockerized" development environment, or set up one directly on your machine. Unlike other tools "dockerized" is a non-intrusive guest on your machine.
- **Caching** - "dockerized" can cache the build environment to speed up builds on CI pipelines.

See the [Quick Start tutorial](tutorials/quick_start.md) to get started!
