import textwrap
import unittest
import tempfile
from pathlib import Path
from shutil import rmtree

from dockerized.core.commands.init import InitCommand
from dockerized.core.commands.errors import CommandError


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
        with self.assertRaisesRegex(CommandError, 'Refusing to overwrite .dockerized'):
            init_command.run()

    def test_creates_dockerfile(self):
        init_command = InitCommand(self.temp_dir)
        init_command.run()
        dockerfile_path = self.temp_dir.joinpath('.dockerized').joinpath('Dockerfile.dockerized')
        self.assertTrue(dockerfile_path.is_file())
        self.assertEqual(dockerfile_path.read_text(), textwrap.dedent("""
        FROM busybox
        # Add your build dependencies here
        """))

    def test_creates_composefile(self):
        init_command = InitCommand(self.temp_dir)
        init_command.run()
        composefile_path = self.temp_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml')
        self.assertTrue(composefile_path.is_file())
        self.assertEqual(composefile_path.read_text(), textwrap.dedent("""
        version: '3.2'
        services:
          dockerized:
            # to enable caching, uncomment and set this:
            # image: <IMAGE_IDENTIFIER>
            build:
              context: .
              dockerfile: Dockerfile.dockerized
              # to enable caching, uncomment and set this:
              # cache_from:
              #   - <IMAGE_IDENTIFIER>
            entrypoint:
              - sh
              - '-c'
        """))

    def test_creates_gitignore(self):
        init_command = InitCommand(self.temp_dir)
        init_command.run()
        gitignore_path = self.temp_dir.joinpath('.dockerized').joinpath('.gitignore')
        self.assertTrue(gitignore_path.is_file())
        self.assertEqual(gitignore_path.read_text(), textwrap.dedent("""
            lock
            prepared
            """))


if __name__ == '__main__':
    unittest.main()
