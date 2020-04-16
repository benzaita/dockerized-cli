from pathlib import Path
from adapters.dockercompose import DockerCompose
from adapters.environment import Environment
from core.commands.errors import CommandError


class DockerComposeCommand:
    docker_compose: DockerCompose
    env: Environment
    project_dir: Path

    def __init__(self):
        self.env = Environment()
        self.project_dir = self.env.get_project_dir()
        if self.project_dir is None:
            raise CommandError("Not inside a Dockerized project directory. Did you run 'dockerized init'?")
        self.docker_compose = DockerCompose(
            composefile=self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            project_dir=self.project_dir
        )
