import os
import unittest
import tempfile
from pathlib import Path
from shutil import rmtree
from unittest.mock import patch

from clients.dockercompose import DockerCompose
from core.commands.exec import ExecCommand


class TestExecCommand(unittest.TestCase):
    temp_dir: Path

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        rmtree(self.temp_dir)

    def test_invokes_docker_run(self):
        with patch.object(DockerCompose, 'run', return_value=None) as mock_run:
            exec_command = ExecCommand(self.temp_dir, 'command arg1')
            exec_command.run()
        mock_run.assert_called_once_with(
            composefile=self.temp_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            working_dir=Path(os.getcwd()),
            bind_dir=self.temp_dir,
            command='command arg1'
        )


if __name__ == '__main__':
    unittest.main()
