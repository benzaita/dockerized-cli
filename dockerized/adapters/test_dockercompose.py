from pathlib import Path
from unittest import TestCase
from unittest import mock
import subprocess

from dockerized.adapters.dockercompose import DockerCompose


class MockProcess:
    def wait(self):
        pass


class TestDockerCompose(TestCase):
    def test_run_executes_run(self):
        docker_compose = DockerCompose(
            compose_files=[Path('fake-composefile')],
            project_dir=Path('fake-project-dir'),
            service_name='fake-service-name',
            run_args_template_strings=[
                '--rm',
                '--service-ports',
                '-v', '${project_dir}:${project_dir}',
                '-w', '${working_dir}',
                '${service_name}',
                '${command}'
            ])
        with mock.patch.object(subprocess, 'Popen', return_value=MockProcess()) as mock_Popen:
            docker_compose.run(Path('fake-working-dir'), 'fake-command')
        mock_Popen.assert_called_once_with([
            'docker-compose',
            '-f', 'fake-composefile',
            '--project-name', '92c9986df24fe7bc679bea041fd2722b',
            'run',
            '--rm',
            '--service-ports',
            '-v', 'fake-project-dir:fake-project-dir',
            '-w', 'fake-working-dir',
            'fake-service-name',
            'fake-command'
        ], stdout=mock.ANY, stderr=mock.ANY)
    
    def test_generates_valid_project_name(self):
        docker_compose = DockerCompose(
            compose_files=[Path('fake-composefile')],
            project_dir=Path('FAKE-PROJECT-DIR-/!@#$%^&*()_'),
            service_name='fake-service-name',
            run_args_template_strings=[])
        with mock.patch.object(subprocess, 'Popen', return_value=MockProcess()) as mock_Popen:
            docker_compose.execute_command([])
        mock_Popen.assert_called_once_with([
            'docker-compose',
            '-f', 'fake-composefile',
            '--project-name', '464ae18505ef29b461a0e48cbd12891d',
        ], stdout=mock.ANY, stderr=mock.ANY)

    def test_push_executes_push(self):
        docker_compose = DockerCompose(
            compose_files=[Path('composefile')],
            project_dir=Path('project-dir'),
            service_name='dockerized',
            run_args_template_strings=[])
        with mock.patch.object(subprocess, 'Popen', return_value=MockProcess()) as mock_Popen:
            docker_compose.push()
        mock_Popen.assert_called_once_with([
            'docker-compose',
            '-f', 'composefile',
            '--project-name', '799ca259be9aa3c5749381ba532be1ae',
            'push',
            'dockerized'
        ], stdout=mock.ANY, stderr=mock.ANY)

    def test_pull_executes_pull(self):
        docker_compose = DockerCompose(
            compose_files=[Path('composefile')],
            project_dir=Path('project-dir'),
            service_name='dockerized',
            run_args_template_strings=[])
        with mock.patch.object(subprocess, 'Popen', return_value=MockProcess()) as mock_Popen:
            docker_compose.pull()
        mock_Popen.assert_called_once_with([
            'docker-compose',
            '-f', 'composefile',
            '--project-name', '799ca259be9aa3c5749381ba532be1ae',
            'pull',
            'dockerized'
        ], stdout=mock.ANY, stderr=mock.ANY)

    def test_build_executes_build(self):
        docker_compose = DockerCompose(
            compose_files=[Path('composefile')],
            project_dir=Path('project-dir'),
            service_name='dockerized',
            run_args_template_strings=[])
        with mock.patch.object(subprocess, 'Popen', return_value=MockProcess()) as mock_Popen:
            docker_compose.build()
        mock_Popen.assert_called_once_with([
            'docker-compose',
            '-f', 'composefile',
            '--project-name', '799ca259be9aa3c5749381ba532be1ae',
            'build',
            'dockerized'
        ], stdout=mock.ANY, stderr=mock.ANY)

