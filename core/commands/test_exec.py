import os
import unittest
from pathlib import Path
from unittest.mock import patch

from clients.dockercompose import DockerCompose
from core.commands.exec import ExecCommand


class TestExecCommand(unittest.TestCase):
    def test_invokes_docker_run(self):
        with patch.object(DockerCompose, 'run', return_value=None) as mock_run:
            exec_command = ExecCommand('command arg1')
            exec_command.run()
        working_dir = Path(os.getcwd())
        mock_run.assert_called_once_with(
            composefile=working_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            working_dir=working_dir,
            bind_dir=working_dir,
            command='command arg1'
        )


if __name__ == '__main__':
    unittest.main()
