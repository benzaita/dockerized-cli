from pathlib import Path
import logging

from dockerized.adapters.environment import Environment
from dockerized.core.commands.errors import CommandError

logger = logging.getLogger(__name__)

dockerfile_content = """
FROM busybox
# Add your build dependencies here
"""

composefile_content = """
version: '3.2'
services:
  dockerized:
    # to enable caching, uncomment and set this:
    # image: <IMAGE_IDENTIFIER>
    build:
      context: .
      dockerfile: Dockerfile.dockerized
      # to enable caching, uncomment and set this:
      # cache_from:
      #   - <IMAGE_IDENTIFIER>
    entrypoint:
      - sh
      - '-c'
"""

gitignore_content = """
lock
prepared
"""

readme_content = """
This directory is used by [dockerized](https://github.com/benzaita/dockerized-cli/).
"""

class InitCommand:
    project_dir: Path

    def __init__(self, project_dir, from_spec=None, env=None):
        self.env = env or Environment()
        self.project_dir = project_dir
        self.from_spec = from_spec

    def run(self):
        dockerized_dir = self.project_dir.joinpath('.dockerized')
        if self.env.path_exists(dockerized_dir):
          raise CommandError('Refusing to overwrite .dockerized')


        if self.from_spec:
          logger.info(f"Initializing from {self.from_spec}")
          self.env.clone_dockerized_from_git(self.from_spec, self.project_dir)
        else:
          try:
              self.env.mkdir(dockerized_dir)
          except FileExistsError:
              raise CommandError('Refusing to overwrite .dockerized')

          dockerfile_path = dockerized_dir.joinpath('Dockerfile.dockerized')
          self.env.write_file(dockerfile_path, dockerfile_content)

          composefile_path = dockerized_dir.joinpath('docker-compose.dockerized.yml')
          self.env.write_file(composefile_path, composefile_content)

          gitignore_path = dockerized_dir.joinpath('.gitignore')
          self.env.write_file(gitignore_path, gitignore_content)

          readme_path = dockerized_dir.joinpath('README.md')
          self.env.write_file(readme_path, readme_content)
