import os
import unittest
from pathlib import Path
from unittest.mock import patch

from adapters.dockercompose import DockerCompose
from adapters.environment import Environment
from core.commands.exec import ExecCommand


class TestExecCommand(unittest.TestCase):
    def test_invokes_docker_run(self):
        project_dir = Path('/project-dir')
        working_dir = project_dir.joinpath('sub-dir')
        with patch.object(Environment, 'get_project_dir', return_value=project_dir):
            with patch.object(Environment, 'get_working_dir', return_value=working_dir):
                with patch.object(DockerCompose, 'run', return_value=None) as mock_run:
                    exec_command = ExecCommand('command arg1')
                    exec_command.run()
        mock_run.assert_called_once_with(
            composefile=project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            working_dir=working_dir,
            bind_dir=working_dir,
            command='command arg1'
        )


if __name__ == '__main__':
    unittest.main()
