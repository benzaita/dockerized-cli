import io
import unittest
from pathlib import Path

from clients.dockercompose import DockerCompose


class TestDockerCompose(unittest.TestCase):
    def test_sets_project_name(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        docker_compose = DockerCompose()
        docker_compose.run(
            stdout=stdout,
            stderr=stderr,
            composefile=Path('path-to-compose-file'),
            working_dir=Path('workind-dir'),
            bind_dir=Path('bind-dir'),
            command=['command', 'arg1']
        )
