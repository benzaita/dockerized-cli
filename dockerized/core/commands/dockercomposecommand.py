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

    def __init__(self):
        self.env = Environment()

        self.project_dir = self.env.get_project_dir()
        if self.project_dir is None:
            raise CommandError("Not inside a Dockerized project directory. Did you run 'dockerized init'?")

        self.prepared_flag_path = self.project_dir.joinpath('.dockerized').joinpath('prepared')

        self.docker_compose = DockerCompose(
            composefile=self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            project_dir=self.project_dir
        )

    def is_project_prepared(self):
        return self.prepared_flag_path.exists()

    def set_project_prepared(self, state):
        if state:
            logger.info(f"Marking {self.project_dir} as 'already prepared'")
            self.prepared_flag_path.touch(exist_ok=False)
        else:
            logger.info(f"Marking {self.project_dir} as 'not prepared'")
            try:
                self.prepared_flag_path.unlink()
            except FileNotFoundError:
                pass
