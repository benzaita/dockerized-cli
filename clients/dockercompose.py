import sys
import subprocess
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DockerCompose:
    def run(self, composefile: Path, working_dir: Path, bind_dir: Path, command: str):
        # Why not use the Docker Compose API directly?
        # Because [it is not officially supported](https://github.com/docker/compose/issues/4542#issuecomment-283191533)

        args = [
            'docker-compose',
            '-f',
            composefile,
            'run',
            '--rm',
            'dockerized',
            command
        ]
        logger.info(f"Running: {args}")
        try:
            process = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr)
            exit_code = process.wait()
        except Exception as e:
            logger.error(f"Raised exception: {e}")
            raise e

        logger.info(f"Finished with exit-code {exit_code}")
        return exit_code
