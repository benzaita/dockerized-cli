from pathlib import Path


dockerfile_content = """
FROM busybox
# Add your build dependencies here
"""

class InitError(Exception):
    def __init__(self, message, cause):
        self.message = message
        self.cause = cause


class InitCommand:
    work_dir: Path

    def __init__(self, work_dir):
        self.work_dir = work_dir

    def run(self):
        try:
            self.work_dir.joinpath('.dockerized').mkdir()
        except FileExistsError as err:
            raise InitError('Refusing to overwrite .dockerized', err)

        dockerfile_path = self.work_dir.joinpath('.dockerized').joinpath('Dockerfile.dockerized')
        dockerfile_path.write_text(dockerfile_content)

        composefile_path = self.work_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml')
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
