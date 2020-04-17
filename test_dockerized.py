import re
import subprocess
import os
import shutil
import unittest
import tempfile
from typing import List
from unittest.case import TestCase

# Why?!
# Because Docker Compose [does not have a proper quiet/silent mode](https://github.com/docker/compose/issues/6026)
DOCKER_COMPOSE_OUTPUT_REGEX = [
    re.compile(r'^Creating network .*'),
    re.compile(r'^Image for service .*? was built because it did not already exist..*'),
    re.compile(r'^Building .*'),
    re.compile(r'^Step [0-9]+/[0-9]+ :.*'),
    re.compile(r'^ ---> [0-9a-f]+$'),
    re.compile(r'^Successfully built [0-9a-f]+$'),
    re.compile(r'^Successfully tagged .*:latest$'),
    re.compile(r'^.*?: Pulling from .*'),
    re.compile(r'^Digest: sha256:.*'),
    re.compile(r'^Status: Downloaded newer image for .*'),
]


class AbstractEndToEndTest(TestCase):
    project_dirs: List[str]

    def setUp(self) -> None:
        self.project_dirs = []
        self.add_project_dir()

    def tearDown(self) -> None:
        for path in self.project_dirs:
            self.run_dockerized('clean', project_dir=path)
            shutil.rmtree(path)

    def run_dockerized(self, cmd_line, working_dir=None, project_dir=None):
        safe_project_dir = project_dir or self.project_dirs[0]
        this_file_path = os.path.dirname(os.path.realpath(__file__))
        dockerized = this_file_path + '/dockerized.py'
        cwd = safe_project_dir if working_dir is None else f"{safe_project_dir}/{working_dir}"
        process = subprocess.run(f"{dockerized} {cmd_line}", cwd=cwd, shell=True, capture_output=True)
        return process.returncode, process.stdout, process.stderr

    def assert_dockerized(self, command, expected_exit_code, expected_stdout, expected_stderr, fixture_name=None,
                          working_dir=None, project_dir=None):
        safe_project_dir = project_dir or self.project_dirs[0]
        if fixture_name is not None:
            if fixture_name == '_init':
                self.run_dockerized('init')
            else:
                self.setup_project_dir(fixture_name, safe_project_dir)
        exit_code, stdout, stderr = self.run_dockerized(command, working_dir)
        filtered_stdout = self.__filter_docker_compose_output(stdout)
        filtered_stderr = self.__filter_docker_compose_output(stderr)
        self.assertEqual(expected_stderr, filtered_stderr)
        self.assertEqual(expected_stdout, filtered_stdout)
        self.assertEqual(expected_exit_code, exit_code)

    def add_project_dir(self):
        path = tempfile.mkdtemp()
        self.project_dirs.append(path)
        return path

    def setup_project_dir(self, fixture_name, project_dir):
        shutil.rmtree(project_dir)

        this_file_path = os.path.dirname(os.path.realpath(__file__))
        shutil.copytree(this_file_path + '/fixtures/' + fixture_name, project_dir)

    def __filter_docker_compose_output(self, output):
        output_str = output.decode('utf-8')
        output_lines = output_str.splitlines()
        filtered_lines = filter(lambda line: not __class__.__is_docker_compose_output_line(line), output_lines)
        return '\n'.join(filtered_lines)

    @staticmethod
    def __is_docker_compose_output_line(line):
        for regex in DOCKER_COMPOSE_OUTPUT_REGEX:
            if regex.match(line):
                return True

        return False


class EndToEndTest(AbstractEndToEndTest):

    def test_init_succeeds(self):
        self.assert_dockerized(
            command='init',
            expected_exit_code=0,
            expected_stdout='created',
            expected_stderr=''
        )

    def test_init_fails(self):
        self.run_dockerized('init')
        self.assert_dockerized(
            command='init',
            expected_exit_code=1,
            expected_stdout='',
            expected_stderr='Refusing to overwrite .dockerized'
        )

    def test_compose_delegates_to_docker_compose(self):
        self.assert_dockerized(
            fixture_name='_init',
            command='compose ps --services',
            expected_exit_code=0,
            expected_stdout='dockerized',
            expected_stderr=''
        )

    def test_compose_exit_code(self):
        self.assert_dockerized(
            fixture_name='_init',
            command='compose kill foo',
            expected_exit_code=1,
            expected_stdout='',
            expected_stderr='No such service: foo'
        )

    def test_exec_exit_code(self):
        self.assert_dockerized(
            fixture_name='_init',
            command='exec exit 42',
            expected_exit_code=42,
            expected_stdout='',
            expected_stderr='',
        )

    def test_exec_pipes_stdout(self):
        self.assert_dockerized(
            fixture_name='_init',
            command='exec echo something out',
            expected_exit_code=0,
            expected_stdout='something out',
            expected_stderr='',
        )

    def test_exec_pipes_stderr(self):
        self.assert_dockerized(
            fixture_name='_init',
            command='exec echo \'something err >&2\'',
            expected_exit_code=0,
            expected_stdout='',
            expected_stderr='something err',
        )

    def test_exec_takes_env_vars_from_docker_compose_file(self):
        self.assert_dockerized(
            fixture_name='with_foo_env_var',
            command='exec echo FOO=\\$FOO',
            expected_exit_code=0,
            expected_stdout='FOO=1',
            expected_stderr='',
        )

    def test_exec_passes_the_command_line_verbatim(self):
        self.assert_dockerized(
            fixture_name='with_foo_env_var',
            command='exec \'env FOO=2 | grep FOO\'',
            expected_exit_code=0,
            expected_stdout='FOO=2',
            expected_stderr='',
        )

    def test_exec_binds_project_dir(self):
        self.assert_dockerized(
            fixture_name='with_files',
            command='exec cat dir/file.txt',
            expected_exit_code=0,
            expected_stdout='Hello world!',
            expected_stderr='',
        )

    def test_exec_runs_from_sub_dir(self):
        self.assert_dockerized(
            fixture_name='with_files',
            working_dir='dir',
            command='exec cat file.txt',
            expected_exit_code=0,
            expected_stdout='Hello world!',
            expected_stderr='',
        )

    def test_exec_makes_the_entire_project_dir_available_in_the_container(self):
        self.assert_dockerized(
            fixture_name='with_files',
            working_dir='dir',
            command='exec cat ../file_in_project_root.txt',
            expected_exit_code=0,
            expected_stdout='Hello from project root',
            expected_stderr='',
        )

    def test_exec_fails_when_not_in_project_sub_dir(self):
        self.assert_dockerized(
            fixture_name='with_no_project',
            command='exec true',
            expected_exit_code=1,
            expected_stdout='',
            expected_stderr='Not inside a Dockerized project directory. Did you run \'dockerized init\'?',
        )

    def test_exec_takes_command_with_args(self):
        self.assert_dockerized(
            fixture_name='with_files',
            command='exec id -u',
            expected_exit_code=0,
            expected_stdout='0',
            expected_stderr='',
        )

    def test_exec_in_two_dirs_does_not_conflict(self):
        foo_dir = self.add_project_dir()
        bar_dir = self.add_project_dir()

        self.setup_project_dir('with_foo_in_dockerfile', foo_dir)
        self.setup_project_dir('with_bar_in_dockerfile', bar_dir)

        self.run_dockerized('exec true', project_dir=foo_dir)
        self.run_dockerized('exec true', project_dir=bar_dir)

        _, stdout_foo, stderr_foo = self.run_dockerized('exec \'echo $TEST_VAR\'', project_dir=foo_dir)
        _, stdout_bar, stderr_bar = self.run_dockerized('exec \'echo $TEST_VAR\'', project_dir=bar_dir)

        self.assertEqual(b'', stderr_foo)
        self.assertEqual(b'', stderr_bar)

        self.assertEqual(b'foo\n', stdout_foo)
        self.assertEqual(b'bar\n', stdout_bar)


if __name__ == '__main__':
    unittest.main()
