from pathlib import Path
from typing import List


class DockerCompose:
    def run(self, stdout, stderr, composefile: Path, bind_dir: Path, command: List[str]):
        stdout.write('something out')
        stderr.write('something err')
        return 42
