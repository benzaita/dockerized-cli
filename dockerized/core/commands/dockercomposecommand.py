import logging
from pathlib import Path
from typing import List
from dockerized.adapters.dockercompose import DockerCompose
from dockerized.adapters.environment import Environment
from dockerized.core.commands.errors import CommandError
from dockerized.core.project import Project

logger = logging.getLogger(__name__)

class DockerizedConfig:
    project_dir: Path
    config_dict: dict

    def __init__(self, project_dir: Path, config_dict: dict):
        self.project_dir = project_dir
        self.config_dict = config_dict
    
    def compose_files(self) -> List[Path]:
        to_path_relative_to_project = lambda s: self.project_dir.joinpath('.dockerized').joinpath(s)
        
        return list(map(to_path_relative_to_project, self.config_dict['compose_files']))

    def service_name(self) -> str:
        return self.config_dict['service_name']


class DockerComposeCommand:
    docker_compose: DockerCompose
    env: Environment
    project_dir: Path

    def __init__(self, env=None, docker_compose=None):
        self.env = env or Environment()

        self.project_dir = self.env.get_project_dir()
        if self.project_dir is None:
            raise CommandError("Not inside a Dockerized project directory. Did you run 'dockerized init'?")

        self.config = DockerizedConfig(self.project_dir, {
            'compose_files': ['./docker-compose.dockerized.yml'],
            'service_name': 'dockerized'
        })

        self.docker_compose = docker_compose or DockerCompose(
            composefiles=self.config.compose_files(),
            project_dir=self.project_dir,
            service_name=self.config.service_name()
        )

        self.project = Project(project_dir=self.project_dir, env=self.env, docker_compose=self.docker_compose)

