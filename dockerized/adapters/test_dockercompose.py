from pathlib import Path
from unittest import TestCase
from unittest import mock
import subprocess

from dockerized.adapters.dockercompose import DockerCompose


class MockProcess:
    def wait(self):
        pass


class TestDockerCompose(TestCase):
    def test_run_executed_run(self):
        docker_compose = DockerCompose(Path('composefile'), Path('project-dir'))
        with mock.patch.object(subprocess, 'Popen', return_value=MockProcess()) as mock_Popen:
            docker_compose.run(Path('working-dir'), 'command')
        mock_Popen.assert_called_once_with([
            'docker-compose',
            '-f', 'composefile',
            '--project-name', 'project-dir',
            'run',
            '--rm',
            '-v', 'project-dir:project-dir',
            '-w', 'working-dir',
            'dockerized',
            'command'
        ], stdout=mock.ANY, stderr=mock.ANY, env=mock.ANY)

    def test_push_executes_push(self):
        docker_compose = DockerCompose(Path('composefile'), Path('project-dir'))
        with mock.patch.object(subprocess, 'Popen', return_value=MockProcess()) as mock_Popen:
            docker_compose.push()
        mock_Popen.assert_called_once_with([
            'docker-compose',
            '-f', 'composefile',
            '--project-name', 'project-dir',
            'push',
            'dockerized'
        ], stdout=mock.ANY, stderr=mock.ANY, env=mock.ANY)

    def test_build_executes_build(self):
        docker_compose = DockerCompose(Path('composefile'), Path('project-dir'))
        with mock.patch.object(subprocess, 'Popen', return_value=MockProcess()) as mock_Popen:
            docker_compose.build()
        mock_Popen.assert_called_once_with([
            'docker-compose',
            '-f', 'composefile',
            '--project-name', 'project-dir',
            'build',
            '--build-arg',
            'BUILDKIT_INLINE_CACHE=1',
            'dockerized'
        ], stdout=mock.ANY, stderr=mock.ANY, env=mock.ANY)
        self.assertTrue(
            set({
                'COMPOSE_DOCKER_CLI_BUILD': '1',
                'DOCKER_BUILDKIT': '1',
            }.items()).issubset(
                set(mock_Popen.call_args[1]['env'].items())
            )
        )

