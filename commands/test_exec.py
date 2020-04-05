import io
import sys
import unittest
import tempfile
from pathlib import Path
from shutil import rmtree
from unittest.mock import patch

from clients.docker import DockerClient
from commands.exec import ExecCommand


class TestExecCommand(unittest.TestCase):
    temp_dir: Path

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()

    def tearDown(self) -> None:
        rmtree(self.temp_dir)

    def test_invokes_docker_run(self):
        with patch.object(DockerClient, 'run', return_value=None) as mock_run:
            exec_command = ExecCommand(self.temp_dir, self.stdout, self.stderr, ['command', 'arg1'])
            exec_command.run()
        mock_run.assert_called_once_with(self.stdout, self.stderr, ['command', 'arg1'])


if __name__ == '__main__':
    unittest.main()
