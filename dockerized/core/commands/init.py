from pathlib import Path

from dockerized.adapters.environment import Environment
from dockerized.core.commands.errors import CommandError

dockerfile_content = """
FROM busybox
# Add your build dependencies here
"""

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

gitignore_content = """
lock
prepared
"""


class InitCommand:
    project_dir: Path

    def __init__(self, project_dir, env=None):
        self.env = env or Environment()
        self.project_dir = project_dir

    def run(self):
        try:
            self.env.mkdir(self.project_dir.joinpath('.dockerized'))
        except FileExistsError:
            raise CommandError('Refusing to overwrite .dockerized')

        dockerfile_path = self.project_dir.joinpath('.dockerized').joinpath('Dockerfile.dockerized')
        self.env.write_file(dockerfile_path, dockerfile_content)

        composefile_path = self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml')
        self.env.write_file(composefile_path, composefile_content)

        gitignore_path = self.project_dir.joinpath('.dockerized').joinpath('.gitignore')
        self.env.write_file(gitignore_path, gitignore_content)
