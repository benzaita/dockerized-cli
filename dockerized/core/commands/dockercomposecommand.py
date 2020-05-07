import logging
from pathlib import Path
from dockerized.adapters.dockercompose import DockerCompose
from dockerized.adapters.environment import Environment
from dockerized.core.commands.errors import CommandError
from dockerized.core.project import Project

logger = logging.getLogger(__name__)


class DockerComposeCommand:
    docker_compose: DockerCompose
    env: Environment
    project_dir: Path

    def __init__(self, env=None, docker_compose=None):
        self.env = env or Environment()

        self.project_dir = self.env.get_project_dir()
        if self.project_dir is None:
            raise CommandError("Not inside a Dockerized project directory. Did you run 'dockerized init'?")

        self.docker_compose = docker_compose or DockerCompose(
            composefile=self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            project_dir=self.project_dir
        )

        self.project = Project(project_dir=self.project_dir, env=self.env, docker_compose=self.docker_compose)

