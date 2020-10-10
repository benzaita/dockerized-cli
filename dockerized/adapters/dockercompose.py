import sys
import subprocess
from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)


class DockerCompose:
    def __init__(self, compose_files: List[Path], project_dir: Path, service_name: str):
        self.compose_files = compose_files
        self.project_dir = project_dir
        self.service_name = service_name

    def run(self, working_dir: Path, command: str):
        docker_compose_args = [
            'run',
            '--rm',
            '-v', f"{str(self.project_dir)}:{str(self.project_dir)}",
            '-w', str(working_dir),
            self.service_name,
            command
        ]
        exit_code = self.execute_command(docker_compose_args)
        return exit_code

    def down(self):
        return self.execute_command(['down'])

    def push(self):
        return self.execute_command(['push', self.service_name])

    def pull(self):
        return self.execute_command(['pull', self.service_name])

    def build(self):
        return self.execute_command(['build', self.service_name])

    def execute_command(self, docker_compose_args):
        # Why not use the Docker Compose API directly?
        # Because [it is not officially supported](https://github.com/docker/compose/issues/4542#issuecomment-283191533)
        args = [
            'docker-compose',
            *self.__get_compose_filename_args(self.compose_files),
            '--project-name', str(self.project_dir)
        ]
        args.extend(docker_compose_args)
        logger.info(f"Running: {args}")
        try:
            process = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr)
            exit_code = process.wait()
        except Exception as e:
            logger.error(f"Raised exception: {e}")
            raise e
        logger.info(f"Finished with exit-code {exit_code}")
        return exit_code

    def __get_compose_filename_args(self, compose_files: List[Path]):
        args = []
        for file in compose_files:
            args.append('-f')
            args.append(str(file))
        return args