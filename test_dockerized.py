import os
import shutil
import unittest
import tempfile

from click.testing import CliRunner
from dockerized import cli


class TestCli(unittest.TestCase):
    runner: CliRunner
    temp_dir: str

    def setUp(self) -> None:
        self.runner = CliRunner(mix_stderr=False)
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_init_succeeds(self):
        result = self.runner.invoke(cli, ['init'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'created\n')

    def test_init_fails(self):
        self.runner.invoke(cli, ['init'])
        result = self.runner.invoke(cli, ['init'])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.stderr, 'Refusing to overwrite .dockerized\n')

    def test_exec_exit_code(self):
        result = self.runner.invoke(cli, ['exec', 'exit', '42'])
        self.assertEqual(result.exit_code, 42)

    def test_exec_pipes_stdout(self):
        result = self.runner.invoke(cli, ['exec', 'echo', 'something out'])
        self.assertEqual(result.stdout, 'something out')

    def test_exec_pipes_stderr(self):
        self.runner.isolation()
        result = self.runner.invoke(cli, args=['exec', 'echo', 'something err', '>&2'], mix_stderr=False)
        self.assertEqual(result.stderr, 'something err')


if __name__ == '__main__':
    unittest.main()
