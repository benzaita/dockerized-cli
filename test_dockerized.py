import re
import subprocess
import os
import unittest
from concurrent.futures.thread import ThreadPoolExecutor

from dockerized.test import ProjectAwareTestCase


class AbstractEndToEndTest(ProjectAwareTestCase):
    def tearDown(self) -> None:
        for path in self.project_dirs:
            self.run_dockerized('clean', project_dir=path)
        super().tearDown()

    def run_dockerized(self, cmd_line, working_dir=None, project_dir=None, env=None):
        safe_project_dir = project_dir or self.project_dirs[0]
        this_file_path = os.path.dirname(os.path.realpath(__file__))
        dockerized = this_file_path + '/dockerized.py'
        cwd = safe_project_dir if working_dir is None else f"{safe_project_dir}/{working_dir}"
        process = subprocess.run(f"{dockerized} {cmd_line}", cwd=cwd, shell=True, capture_output=True, env=env)
        return process.returncode, process.stdout, process.stderr

    def assert_dockerized(self, command, expected_exit_code=None, fixture_name=None, working_dir=None, project_dir=None,
                          expected_stderr_regex=None, expected_stdout_regex=None, env=None):
        safe_project_dir = project_dir or self.project_dirs[0]
        if fixture_name is not None:
            if fixture_name == '_init':
                self.run_dockerized('init')
            else:
                self.setup_project_dir(fixture_name, safe_project_dir)
        exit_code, stdout, stderr = self.run_dockerized(command, working_dir, env=env)

        self.assertRegex(stderr.decode('utf-8'), re.compile(expected_stderr_regex, re.MULTILINE))
        self.assertRegex(stdout.decode('utf-8'), re.compile(expected_stdout_regex, re.MULTILINE))
        self.assertEqual(expected_exit_code, exit_code)


class EndToEndTest(AbstractEndToEndTest):

    def test_init_succeeds(self):
        self.assert_dockerized(
            command='init',
            expected_exit_code=0,
            expected_stdout_regex=r'^created$',
            expected_stderr_regex=r'.*'
        )

    def test_init_from(self):
        self.assert_dockerized(
            command='init --from https://github.com/benzaita/dockerized-example-golang.git',
            expected_exit_code=0,
            expected_stdout_regex=r'^initialized .dockerized/ from https://github.com/benzaita/dockerized-example-golang.git',
            expected_stderr_regex=r'^$'
        )

    def test_init_fails(self):
        self.run_dockerized('init')
        self.assert_dockerized(
            command='init',
            expected_exit_code=1,
            expected_stdout_regex=r'.*',
            expected_stderr_regex=r'^Refusing to overwrite .dockerized$'
        )

    def test_compose_delegates_to_docker_compose(self):
        self.assert_dockerized(
            fixture_name='_init',
            command='compose ps --services',
            expected_exit_code=0,
            expected_stdout_regex=r'^dockerized$',
            expected_stderr_regex=r'.*'
        )

    def test_compose_exit_code(self):
        self.assert_dockerized(
            fixture_name='_init',
            command='compose kill foo',
            expected_exit_code=1,
            expected_stdout_regex=r'.*',
            expected_stderr_regex=r'^No such service: foo$'
        )

    def test_exec_exit_code(self):
        self.assert_dockerized(
            fixture_name='_init',
            command='exec exit 42',
            expected_exit_code=42,
            expected_stdout_regex=r'.*',
            expected_stderr_regex=r'.*',
        )

    def test_exec_pipes_stdout(self):
        self.assert_dockerized(
            fixture_name='_init',
            command='exec echo something out',
            expected_exit_code=0,
            expected_stdout_regex=r'^something out$',
            expected_stderr_regex=r'.*',
        )

    def test_exec_pipes_stderr(self):
        self.assert_dockerized(
            fixture_name='_init',
            command='exec echo \'something err >&2\'',
            expected_exit_code=0,
            expected_stdout_regex=r'.*',
            expected_stderr_regex=r'something err',
        )

    def test_exec_takes_env_vars_from_docker_compose_file(self):
        self.assert_dockerized(
            fixture_name='with_foo_env_var',
            command='exec echo FOO=\\$FOO',
            expected_exit_code=0,
            expected_stdout_regex=r'^FOO=1$',
            expected_stderr_regex=r'.*',
        )

    def test_exec_passes_the_command_line_verbatim(self):
        self.assert_dockerized(
            fixture_name='with_foo_env_var',
            command='exec \'env FOO=2 | grep FOO\'',
            expected_exit_code=0,
            expected_stdout_regex=r'^FOO=2$',
            expected_stderr_regex=r'.*',
        )

    def test_exec_binds_project_dir(self):
        self.assert_dockerized(
            fixture_name='with_files',
            command='exec cat dir/file.txt',
            expected_exit_code=0,
            expected_stdout_regex=r'^Hello world!$',
            expected_stderr_regex=r'.*',
        )

    def test_exec_runs_from_sub_dir(self):
        self.assert_dockerized(
            fixture_name='with_files',
            working_dir='dir',
            command='exec cat file.txt',
            expected_exit_code=0,
            expected_stdout_regex=r'^Hello world!$',
            expected_stderr_regex=r'.*',
        )

    def test_exec_makes_the_entire_project_dir_available_in_the_container(self):
        self.assert_dockerized(
            fixture_name='with_files',
            working_dir='dir',
            command='exec cat ../file_in_project_root.txt',
            expected_exit_code=0,
            expected_stdout_regex=r'^Hello from project root$',
            expected_stderr_regex=r'.*',
        )

    def test_exec_fails_when_not_in_project_sub_dir(self):
        self.assert_dockerized(
            fixture_name='with_no_project',
            command='exec true',
            expected_exit_code=1,
            expected_stdout_regex=r'.*',
            expected_stderr_regex=r'^Not inside a Dockerized project directory. Did you run \'dockerized init\'\?$',
        )

    def test_exec_takes_command_with_args(self):
        self.assert_dockerized(
            fixture_name='with_files',
            command='exec id -u',
            expected_exit_code=0,
            expected_stdout_regex=r'^0$',
            expected_stderr_regex=r'.*',
        )

    def test_exec_in_two_dirs_does_not_conflict(self):
        foo_dir = self.add_project_dir()
        bar_dir = self.add_project_dir()

        self.setup_project_dir('with_foo_in_dockerfile', foo_dir)
        self.setup_project_dir('with_bar_in_dockerfile', bar_dir)

        self.run_dockerized('exec true', project_dir=foo_dir)
        self.run_dockerized('exec true', project_dir=bar_dir)

        _, stdout_foo, _ = self.run_dockerized('exec \'echo $TEST_VAR\'', project_dir=foo_dir)
        _, stdout_bar, _ = self.run_dockerized('exec \'echo $TEST_VAR\'', project_dir=bar_dir)

        self.assertEqual(b'foo\n', stdout_foo)
        self.assertEqual(b'bar\n', stdout_bar)

    def test_exec_parallel_invocations_prepare_only_once(self):
        project_dir = self.add_project_dir()
        self.setup_project_dir('with_foo_in_dockerfile', project_dir=project_dir)

        num_of_parallel_invocations = 10
        futures = [None] * num_of_parallel_invocations

        print(f"Running {num_of_parallel_invocations} exec commands in parallel")
        with ThreadPoolExecutor(max_workers=num_of_parallel_invocations) as executor:
            for i in range(num_of_parallel_invocations):
                futures[i] = executor.submit(lambda: self.run_dockerized('exec true', project_dir=project_dir))

        results = [f.result() for f in futures]

        exit_codes = [r[0] for r in results]
        stdouts = [r[1].decode('utf-8') for r in results]
        stderrs = [r[2].decode('utf-8') for r in results]

        non_zero_exit_codes = [c for c in exit_codes if c != 0]
        non_empty_stdouts = [s for s in stdouts if len(s) > 0]
        non_empty_stderrs = [s for s in stderrs if re.search(r'Creating network', s) is not None]

        self.assertTrue(len(non_empty_stderrs) == 1,
                        f"Expected only one STDERR to be not empty, got {len(non_empty_stderrs)}:\n" +
                        '\n---\n'.join(non_empty_stderrs))

        self.assertTrue(len(non_empty_stdouts) == 1,
                        f"Expected only one STDOUT to be not empty, got {len(non_empty_stdouts)}:\n" +
                        '\n---\n'.join(non_empty_stdouts))

        self.assertTrue(len(non_zero_exit_codes) == 0,
                        f"Expected all exit codes to be zero, got: {','.join(map(str, non_zero_exit_codes))}")

    # TODO why does this test fail on CI but succeed locally?
    # def test_exec_uses_build_cache(self):
    #     subprocess.run('docker rmi docker.pkg.github.com/benzaita/dockerized-cli/fixture-with_build_cache:latest', shell=True)
    #     self.assert_dockerized(
    #         fixture_name='with_build_cache',
    #         command='--loglevel INFO exec true',
    #         expected_exit_code=0,
    #         expected_stdout_regex=''.join([
    #             r'Step 2/2 : RUN echo "long operation"\n',
    #             r' ---> Using cache\n',
    #         ]),
    #         expected_stderr_regex=r'Pulling dockerized',
    #     )

    def test_allows_config_file(self):
        self.assert_dockerized(
            fixture_name='with_config',
            command='exec true',
            expected_exit_code=0,
            expected_stdout_regex=r'.*',
            expected_stderr_regex=r'.*',
        )

if __name__ == '__main__':
    unittest.main()
