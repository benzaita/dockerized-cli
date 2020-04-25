from pathlib import Path
from unittest.mock import MagicMock

from dockerized.adapters.dockercompose import DockerCompose
from dockerized.adapters.environment import Environment
from dockerized.core.project import Project
from dockerized.test import ProjectAwareTestCase


class TestProject(ProjectAwareTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.setup_project_dir(fixture_name='with_files', project_dir=self.project_dirs[0])

    def test_prepare_runs_if_needed(self):
        project_dir = Path(self.project_dirs[0])

        env = Environment()

        docker_compose = DockerCompose(Path(composefile='mock-compose-file'), project_dir=project_dir)
        docker_compose.pull = MagicMock()
        docker_compose.run = MagicMock()

        project = Project(project_dir=project_dir, env=env, docker_compose=docker_compose)
        project.set_prepared(False)
        project.prepare_if_needed()

        docker_compose.pull.assert_called_once_with()
        docker_compose.run.assert_called_once_with(working_dir=project_dir, command='true')

    def test_prepare_ignores_pull_errors(self):
        project_dir = Path(self.project_dirs[0])

        env = Environment()

        docker_compose = DockerCompose(Path(composefile='mock-compose-file'), project_dir=project_dir)
        docker_compose.pull = MagicMock(return_value=1)
        docker_compose.run = MagicMock()

        project = Project(project_dir=project_dir, env=env, docker_compose=docker_compose)
        project.set_prepared(False)
        project.prepare_if_needed()

        docker_compose.pull.assert_called_once_with()
        docker_compose.run.assert_called_once_with(working_dir=project_dir, command='true')

    def test_prepare_does_not_runs_if_not_needed(self):
        project_dir = Path(self.project_dirs[0])

        env = Environment()

        docker_compose = DockerCompose(Path(composefile='mock-compose-file'), project_dir=project_dir)
        docker_compose.pull = MagicMock()
        docker_compose.run = MagicMock()

        project = Project(project_dir=project_dir, env=env, docker_compose=docker_compose)
        project.set_prepared(True)
        project.prepare_if_needed()

        docker_compose.pull.assert_not_called()
        docker_compose.run.assert_not_called()


