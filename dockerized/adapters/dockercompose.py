import sys
import subprocess
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DockerCompose:
    def __init__(self, composefile: Path, project_dir: Path):
        self.composefile = composefile
        self.project_dir = project_dir

    def run(self, working_dir: Path, command: str):
        docker_compose_args = [
            'run',
            '--rm',
            '-v', f"{str(self.project_dir)}:{str(self.project_dir)}",
            '-w', str(working_dir),
            'dockerized',
            command
        ]
        exit_code = self.execute_command(docker_compose_args)
        return exit_code

    def down(self):
        return self.execute_command(['down'])

    def push(self):
        return self.execute_command(['push', 'dockerized'])

    def pull(self):
        return self.execute_command(['pull', 'dockerized'])

    def build(self):
        return self.execute_command(['build', 'dockerized'])

    def execute_command(self, docker_compose_args):
        # Why not use the Docker Compose API directly?
        # Because [it is not officially supported](https://github.com/docker/compose/issues/4542#issuecomment-283191533)
        args = [
            'docker-compose',
            '-f', str(self.composefile),
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

