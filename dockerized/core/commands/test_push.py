import unittest
from pathlib import Path
from unittest.mock import MagicMock

from dockerized.core.commands.push import PushCommand
from dockerized.adapters.dockercompose import DockerCompose
from dockerized.adapters.environment import Environment


class TestPushCommand(unittest.TestCase):
    def test_runs_docker_compose(self):
        project_dir = Path('/project-dir')
        working_dir = project_dir.joinpath('sub-dir')

        env = Environment()
        env.get_project_dir = MagicMock(return_value=project_dir)
        env.get_working_dir = MagicMock(return_value=working_dir)
        env.unlink_file = MagicMock()

        docker_compose = DockerCompose(compose_files=[Path('compose-file')], project_dir=project_dir, service_name='dockerized')
        docker_compose.push = MagicMock()

        push_command = PushCommand(env=env, docker_compose=docker_compose)
        push_command.run()

        docker_compose.push.assert_called_once_with()
