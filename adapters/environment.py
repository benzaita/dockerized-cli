import os
from pathlib import Path


class Environment:
    def get_project_dir(self):
        return self.get_working_dir()

    def get_working_dir(self):
        return Path(os.getcwd())
