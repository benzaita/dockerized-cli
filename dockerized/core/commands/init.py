from pathlib import Path
from dockerized.core.commands.errors import CommandError

dockerfile_content = """
FROM busybox
# Add your build dependencies here
"""


class InitCommand:
    project_dir: Path

    def __init__(self, project_dir):
        self.project_dir = project_dir

    def run(self):
        try:
            self.project_dir.joinpath('.dockerized').mkdir()
        except FileExistsError as err:
            raise CommandError('Refusing to overwrite .dockerized')

        dockerfile_path = self.project_dir.joinpath('.dockerized').joinpath('Dockerfile.dockerized')
        dockerfile_path.write_text(dockerfile_content)

        composefile_path = self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml')
        composefile_content = """
version: '2'
services:
  dockerized:
    build:
      context: .
      dockerfile: Dockerfile.dockerized
    entrypoint:
      - sh
      - '-c'
"""
        composefile_path.write_text(composefile_content)
