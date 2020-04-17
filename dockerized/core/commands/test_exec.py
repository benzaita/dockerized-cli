import unittest
from pathlib import Path
from unittest.mock import patch

from dockerized.adapters.dockercompose import DockerCompose
from dockerized.adapters.environment import Environment
from dockerized.core.commands.exec import ExecCommand
from dockerized.core.commands.errors import CommandError


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
            working_dir=working_dir,
            command='command arg1'
        )

    def test_fails_when_not_in_project(self):
        working_dir = Path('working-dir')
        with patch.object(Environment, 'get_project_dir', return_value=None):
            with patch.object(Environment, 'get_working_dir', return_value=working_dir):
                with patch.object(DockerCompose, 'run', return_value=None) as mock_run:
                    self.assertRaisesRegex(CommandError, 'Not inside a Dockerized project directory. Did you run '
                                                      '\'dockerized init\'?', lambda: ExecCommand('command arg1'))
        mock_run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
