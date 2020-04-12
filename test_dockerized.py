import subprocess
import os
import shutil
import unittest
import tempfile


class TestEndToEnd(unittest.TestCase):
    project_dir: str

    def setUp(self) -> None:
        self.project_dir = tempfile.mkdtemp()
        os.chdir(self.project_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.project_dir)

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
            fixture_name='_init',
            command='exec exit 42',
            expected_exit_code=42,
            expected_stdout=b'',
            expected_stderr=b'',
        )

    def test_exec_pipes_stdout(self):
        self.assertDockerized(
            fixture_name='_init',
            command='exec echo something out',
            expected_exit_code=0,
            expected_stdout=b'something out\n',
            expected_stderr=b'',
        )

    def test_exec_pipes_stderr(self):
        self.assertDockerized(
            fixture_name='_init',
            command='exec echo \'something err >&2\'',
            expected_exit_code=0,
            expected_stdout=b'',
            expected_stderr=b'something err\n',
        )

    def test_exec_takes_env_vars_from_docker_compose_file(self):
        self.assertDockerized(
            fixture_name='with_foo_env_var',
            command='exec echo FOO=\\$FOO',
            expected_exit_code=0,
            expected_stdout=b'FOO=1\n',
            expected_stderr=b'',
        )

    def test_exec_binds_project_dir(self):
        self.assertDockerized(
            fixture_name='with_files',
            command='exec cat dir/file.txt',
            expected_exit_code=0,
            expected_stdout=b'Hello world!\n',
            expected_stderr=b'',
        )

    def test_exec_runs_from_sub_dir(self):
        self.assertDockerized(
            fixture_name='with_files',
            working_dir='dir',
            command='exec cat file.txt',
            expected_exit_code=0,
            expected_stdout=b'Hello world!\n',
            expected_stderr=b'',
        )

    def test_exec_makes_the_entire_project_dir_available_in_the_container(self):
        self.assertDockerized(
            fixture_name='with_files',
            working_dir='dir',
            command='exec cat ../file_in_project_root.txt',
            expected_exit_code=0,
            expected_stdout=b'Hello from project root\n',
            expected_stderr=b'',
        )

    def test_exec_fails_when_not_in_project_sub_dir(self):
        self.assertDockerized(
            fixture_name='with_no_project',
            command='exec true',
            expected_exit_code=1,
            expected_stdout=b'',
            expected_stderr=b'Not inside a Dockerized project directory. Did you run \'dockerized init\'?\n',
        )

    # TODO test_exec_takes_command_with_args: ls -l

    def assertDockerized(self, command, expected_exit_code, expected_stdout, expected_stderr, fixture_name=None, working_dir=None):
        if fixture_name is not None:
            if fixture_name == '_init':
                self.run_dockerized('init')
            else:
                self.setup_project_dir(fixture_name)
        exit_code, stdout, stderr = self.run_dockerized(command, working_dir)
        self.assertEqual(expected_stderr, stderr)
        self.assertEqual(expected_stdout, stdout)
        self.assertEqual(expected_exit_code, exit_code)

    def run_dockerized(self, cmd_line, working_dir=None):
        this_file_path = os.path.dirname(os.path.realpath(__file__))
        dockerized = this_file_path + '/dockerized.py'
        cwd = self.project_dir if working_dir is None else f"{self.project_dir}/{working_dir}"
        process = subprocess.run(f"{dockerized} {cmd_line}", cwd=cwd, shell=True, capture_output=True)
        return process.returncode, process.stdout, process.stderr

    def setup_project_dir(self, fixture_name):
        shutil.rmtree(self.project_dir)

        this_file_path = os.path.dirname(os.path.realpath(__file__))
        shutil.copytree(this_file_path + '/fixtures/' + fixture_name, self.project_dir)


if __name__ == '__main__':
    unittest.main()
