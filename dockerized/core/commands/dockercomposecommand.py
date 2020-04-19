import logging
from pathlib import Path
from dockerized.adapters.dockercompose import DockerCompose
from dockerized.adapters.environment import Environment
from dockerized.core.commands.errors import CommandError

logger = logging.getLogger(__name__)


class DockerComposeCommand:
    docker_compose: DockerCompose
    env: Environment
    project_dir: Path
    prepared_flag_path: Path

    def __init__(self, env=None, docker_compose=None):
        self.env = env or Environment()

        self.project_dir = self.env.get_project_dir()
        if self.project_dir is None:
            raise CommandError("Not inside a Dockerized project directory. Did you run 'dockerized init'?")

        self.prepared_flag_path = self.project_dir.joinpath('.dockerized').joinpath('prepared')

        self.docker_compose = docker_compose or DockerCompose(
            composefile=self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            project_dir=self.project_dir
        )

    def is_project_prepared(self):
        return self.env.path_exists(self.prepared_flag_path)

    def set_project_prepared(self, state):
        if state:
            logger.info(f"Marking {self.project_dir} as 'already prepared'")
            self.env.touch_file(self.prepared_flag_path)
        else:
            logger.info(f"Marking {self.project_dir} as 'not prepared'")
            try:
                self.env.unlink_file(self.prepared_flag_path)
            except FileNotFoundError:
                pass
