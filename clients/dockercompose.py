from pathlib import Path
from typing import List

# Why not use the Docker Compose API directly?
# Because [it is not officially supported](https://github.com/docker/compose/issues/4542#issuecomment-283191533)


class DockerCompose:
    def run(self, stdout, stderr, composefile: Path, working_dir: Path, bind_dir: Path, command: List[str]):
        stdout.write('something out')
        stderr.write('something err')
        return 42
