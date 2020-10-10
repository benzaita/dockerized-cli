import unittest
from pathlib import Path
from unittest.mock import MagicMock

from dockerized.adapters.dockercompose import DockerCompose
from dockerized.adapters.environment import Environment
from dockerized.core.commands.compose import ComposeCommand


class TestCleanCommand(unittest.TestCase):
    def test_runs_docker_compose(self):
        project_dir = Path('/project-dir')
        working_dir = project_dir.joinpath('sub-dir')
        args = ['arg1', 'arg2']

        env = Environment()
        env.get_project_dir = MagicMock(return_value=project_dir)
        env.get_working_dir = MagicMock(return_value=working_dir)

        docker_compose = DockerCompose(compose_files=[Path('compose-file')], project_dir=project_dir, service_name='dockerized')
        docker_compose.execute_command = MagicMock()

        compose_command = ComposeCommand(args, env=env, docker_compose=docker_compose)
        compose_command.run()

        docker_compose.execute_command.assert_called_once_with(args)
