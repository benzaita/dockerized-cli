import os
from pathlib import Path


class Environment:
    def get_project_dir(self):
        curr_dir = self.get_working_dir()
        while curr_dir != Path.root and not curr_dir.joinpath('.dockerized').is_dir():
            curr_dir = curr_dir.parent

        if curr_dir == Path.root:
            return None
        else:
            return curr_dir

    def get_working_dir(self):
        return Path(os.getcwd())
