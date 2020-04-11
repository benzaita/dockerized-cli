from pathlib import Path
from typing import List
import subprocess

# Why not use the Docker Compose API directly?
# Because [it is not officially supported](https://github.com/docker/compose/issues/4542#issuecomment-283191533)


class DockerCompose:
    def run(self, stdout, stderr, composefile: Path, working_dir: Path, bind_dir: Path, command: List[str]):
        import sys
        try:
            process = subprocess.Popen(' '.join(command), stdout=sys.stdout, stderr=sys.stderr, shell=True)
            return process.wait()
        except Exception as e:
            raise e
