import unittest
import tempfile
from pathlib import Path
from shutil import rmtree

from commands.init import InitCommand, InitError


class TestInitCommand(unittest.TestCase):
    temp_dir: Path

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        rmtree(self.temp_dir)

    def test_creates_dockerized_dir(self):
        init_command = InitCommand(self.temp_dir)
        init_command.run()
        self.assertTrue(self.temp_dir.joinpath('.dockerized').is_dir())

    def test_fails_if_dir_exists(self):
        init_command = InitCommand(self.temp_dir)
        init_command.run()
        with self.assertRaisesRegex(InitError, 'Refusing to overwrite .dockerized'):
            init_command.run()


if __name__ == '__main__':
    unittest.main()
