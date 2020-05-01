import logging
import os
import time
from pathlib import Path


def is_root(path):
    return path == Path('/')


class Environment:
    def get_project_dir(self):
        curr_dir = self.get_working_dir()
        while not is_root(curr_dir) and not curr_dir.joinpath('.dockerized').is_dir():
            logging.debug(f"Searching for '.dockerized' in {curr_dir}")
            curr_dir = curr_dir.parent

        if is_root(curr_dir):
            return None
        else:
            return curr_dir

    def get_working_dir(self):
        return Path(os.getcwd())

    def touch_file(self, path: Path):
        path.touch(exist_ok=True)

    def get_file_modification_time(self, path: Path):
        return time.gmtime(path.stat().st_mtime)

    def unlink_file(self, path: Path):
        path.unlink()

    def path_exists(self, path: Path):
        return path.exists()

    def mkdir(self, path: Path):
        path.mkdir()

    def write_file(self, path: Path, content):
        path.write_text(content)

    def rmdir(self, path: Path):
        path.rmdir()