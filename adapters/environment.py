import logging
import os
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
