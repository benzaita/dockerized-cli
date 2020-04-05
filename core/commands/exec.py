import sys
from pathlib import Path
from typing import List

from clients.dockercompose import DockerCompose


class ExecCommand:
    project_dir: Path
    stdout: object
    stderr: object
    command: List[str]

    def __init__(self, project_dir, stdout, stderr, command):
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.project_dir = project_dir

    def run(self):
        docker_compose = DockerCompose()
        return docker_compose.run(
            stdout=self.stdout,
            stderr=self.stderr,
            composefile=self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            # working_dir=cwd,
            bind_dir=self.project_dir,
            command=self.command
        )
