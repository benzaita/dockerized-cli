from pathlib import Path
from unittest import TestCase
from unittest import mock
import subprocess

from adapters.dockercompose import DockerCompose


class MockProcess:
    def wait(self):
        pass


class TestDockerCompose(TestCase):
    def test_run_adds_dash_rm(self):
        docker_compose = DockerCompose()
        with mock.patch.object(subprocess, 'Popen', return_value=MockProcess()) as mock_Popen:
            docker_compose.run(Path('composefile'), Path('working-dir'), Path('project-dir'), 'command')
        mock_Popen.assert_called_once_with([
            'docker-compose',
            '-f', 'composefile',
            'run',
            '--rm',
            '-v', 'project-dir:project-dir',
            '-w', 'working-dir',
            'dockerized',
            'command'
        ], stdout=mock.ANY, stderr=mock.ANY)
