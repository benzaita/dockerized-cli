import sys
import subprocess
from pathlib import Path

# Why not use the Docker Compose API directly?
# Because [it is not officially supported](https://github.com/docker/compose/issues/4542#issuecomment-283191533)


class DockerCompose:
    def run(self, composefile: Path, working_dir: Path, bind_dir: Path, command: str):
        try:
            args = [
                'docker-compose',
                '-f',
                composefile,
                'run',
                'dockerized',
                command
            ]
            process = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr)
            return process.wait()
        except Exception as e:
            raise e
