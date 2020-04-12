import os
from pathlib import Path

from clients.dockercompose import DockerCompose


class ExecCommand:
    command: str

    def __init__(self, command):
        self.command = command

    def run(self):
        docker_compose = DockerCompose()
        working_dir = Path(os.getcwd())
        return docker_compose.run(
            composefile=working_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            working_dir=working_dir,
            bind_dir=working_dir,
            command=self.command
        )
