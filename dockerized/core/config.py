from pathlib import Path
from typing import List
import yaml
from dockerized.core.errors import DockerizedError
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'compose_files': ['./docker-compose.dockerized.yml'],
    'service_name': 'dockerized'
}

class Config:
    project_dir: Path
    config_dict: dict

    @staticmethod
    def default(project_dir: Path):
        return Config(project_dir, DEFAULT_CONFIG)

    @staticmethod
    def fromYamlFile(config_file: Path):
        project_dir = config_file.parent.parent
        yaml_dict = {}

        logger.info(f"Reading configuration from: {str(config_file)}")

        try:
            with open(config_file, "r") as yaml_file:
                yaml_dict = yaml.safe_load(yaml_file)
        except yaml.YAMLError as e:
            raise DockerizedError(f"Failed to read configuration file ({str(config_file)}): {e}")

        return Config(project_dir, yaml_dict)

    def __init__(self, project_dir: Path, config_dict: dict):
        self.project_dir = project_dir
        self.config_dict = config_dict

    def compose_files(self) -> List[Path]:
        def to_path_relative_to_project(
            s): return self.project_dir.joinpath('.dockerized').joinpath(s)

        return list(map(to_path_relative_to_project, self.config_dict['compose_files']))

    def service_name(self) -> str:
        return self.config_dict['service_name']
