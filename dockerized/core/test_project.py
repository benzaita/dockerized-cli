import time
from pathlib import Path
from unittest.mock import MagicMock

from dockerized.adapters.dockercompose import DockerCompose
from dockerized.adapters.environment import Environment
from dockerized.core.errors import DockerizedError
from dockerized.core.project import Project
from dockerized.test import ProjectAwareTestCase


class TestProject(ProjectAwareTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.setup_project_dir(fixture_name='with_files', project_dir=self.project_dirs[0])
        self.docker_compose_mock = MagicMock(DockerCompose)
        self.docker_compose_mock.build = MagicMock(return_value=0)
        self.project_dir = Path(self.project_dirs[0])
        self.env = Environment()
        self.project = Project(project_dir=self.project_dir, env=self.env, docker_compose=self.docker_compose_mock)

    def test_prepare_runs_if_needed(self):
        self.project.set_prepared(False)
        self.project.prepare_if_needed()

        self.docker_compose_mock.build.assert_called_once_with()
        self.docker_compose_mock.run.assert_called_once_with(working_dir=self.project_dir, command='true')

    def test_prepare_raises_error_if_build_fails(self):
        self.docker_compose_mock.build = MagicMock(return_value=1)

        self.project.set_prepared(False)
        self.assertRaises(DockerizedError, lambda: self.project.prepare_if_needed())

    def test_prepare_does_not_raise_error_if_pull_fails(self):
        self.docker_compose_mock.pull = MagicMock(return_value=1)

        self.project.set_prepared(False)
        self.project.prepare_if_needed()

    def test_prepare_does_not_runs_if_not_needed(self):
        self.project.set_prepared(True)
        self.project.prepare_if_needed()

        self.docker_compose_mock.build.assert_not_called()
        self.docker_compose_mock.run.assert_not_called()

    def test_is_not_prepared_when_Dockerfile_has_changed_since(self):
        self.project.set_prepared(True)
        time.sleep(1)
        self.project_dir.joinpath('.dockerized').joinpath('Dockerfile.dockerized').touch()

        self.assertFalse(self.project.is_prepared())

    def test_is_not_prepared_when_composefile_has_changed_since(self):
        self.project.set_prepared(True)
        time.sleep(1)
        self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml').touch()

        self.assertFalse(self.project.is_prepared())

    def test_is_prepared_when_newer_than_Dockerfile_and_composefile(self):
        self.project_dir.joinpath('.dockerized').joinpath('Dockerfile.dockerized').touch()
        self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml').touch()
        time.sleep(1)
        self.project.set_prepared(True)

        self.assertTrue(self.project.is_prepared())

    def test_is_prepared_can_handle_missing_Dockerfile(self):
        self.project_dir.joinpath('.dockerized').joinpath('Dockerfile.dockerized').unlink()
        self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml').touch()
        time.sleep(1)
        self.project.set_prepared(True)

        self.assertTrue(self.project.is_prepared())
