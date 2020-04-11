import os
import shutil
import unittest
import tempfile


class TestCli(unittest.TestCase):
    temp_dir: str

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_init_succeeds(self):
        self.assertDockerized(
            command='init',
            expected_exit_code=0,
            expected_stdout=b'created\n',
            expected_stderr=b''
        )

    def test_init_fails(self):
        self.run_dockerized('init')
        self.assertDockerized(
            command='init',
            expected_exit_code=1,
            expected_stdout=b'',
            expected_stderr=b'Refusing to overwrite .dockerized\n'
        )

    def test_exec_exit_code(self):
        self.assertDockerized(
            command='exec exit 42',
            expected_exit_code=42,
            expected_stdout=b'',
            expected_stderr=b'',
        )

    def test_exec_pipes_stdout(self):
        self.assertDockerized(
            command='exec echo something out',
            expected_exit_code=0,
            expected_stdout=b'something out\n',
            expected_stderr=b'',
        )

    def test_exec_pipes_stderr(self):
        self.assertDockerized(
            command='exec echo \'something err >&2\'',
            expected_exit_code=0,
            expected_stdout=b'',
            expected_stderr=b'something err\n',
        )

    def assertDockerized(self, command, expected_exit_code, expected_stdout, expected_stderr):
        exit_code, stdout, stderr = self.run_dockerized(command)
        self.assertEqual(expected_stderr, stderr)
        self.assertEqual(expected_stdout, stdout)
        self.assertEqual(expected_exit_code, exit_code)

    def run_dockerized(self, cmd_line):
        import subprocess
        import os
        dockerized = os.path.dirname(os.path.realpath(__file__)) + '/dockerized.py'
        process = subprocess.run(f"{dockerized} {cmd_line}", cwd=self.temp_dir, shell=True, capture_output=True)
        return process.returncode, process.stdout, process.stderr


if __name__ == '__main__':
    unittest.main()
