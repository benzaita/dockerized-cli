from pathlib import Path


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

