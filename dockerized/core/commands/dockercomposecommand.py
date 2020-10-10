import logging
from pathlib import Path
from dockerized.adapters.dockercompose import DockerCompose
from dockerized.adapters.environment import Environment
from dockerized.core.commands.errors import CommandError
from dockerized.core.project import Project
from dockerized.core.config import Config

logger = logging.getLogger(__name__)

class DockerComposeCommand:
    docker_compose: DockerCompose
    env: Environment
    project_dir: Path

    def __init__(self, env=None, docker_compose=None):
        self.env = env or Environment()

        self.project_dir = self.env.get_project_dir()
        if self.project_dir is None:
            raise CommandError("Not inside a Dockerized project directory. Did you run 'dockerized init'?")

        config_file = self.project_dir.joinpath('.dockerized').joinpath('config.yml') 
        if config_file.exists():
            self.config = Config.fromYamlFile(config_file)
        else:
            logger.info(f"Configuration file ({str(config_file)}) does not exist. Using defaults.")
            self.config = Config.default(self.project_dir)

        self.docker_compose = docker_compose or DockerCompose(
            compose_files=self.config.compose_files(),
            project_dir=self.project_dir,
            service_name=self.config.service_name()
        )

        self.project = Project(project_dir=self.project_dir, env=self.env, docker_compose=self.docker_compose)
