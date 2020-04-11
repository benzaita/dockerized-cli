import os
from pathlib import Path

from clients.dockercompose import DockerCompose


class ExecCommand:
    project_dir: Path
    command: str

    def __init__(self, project_dir, command):
        self.command = command
        self.project_dir = project_dir

    def run(self):
        docker_compose = DockerCompose()
        return docker_compose.run(
            composefile=self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            working_dir=Path(os.getcwd()),
            bind_dir=self.project_dir,
            command=self.command
        )
