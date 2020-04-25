import os
import shutil
import tempfile
from unittest.case import TestCase

from typing import List


class ProjectAwareTestCase(TestCase):
    project_dirs: List[str]

    def setUp(self) -> None:
        self.project_dirs = []
        self.add_project_dir()

    def tearDown(self) -> None:
        for path in self.project_dirs:
            shutil.rmtree(path)

    def add_project_dir(self):
        path = tempfile.mkdtemp()
        self.project_dirs.append(path)
        return path

    def setup_project_dir(self, fixture_name, project_dir):
        shutil.rmtree(project_dir)

        fixtures_dir = os.path.dirname(os.path.realpath(__file__)) + '/../../fixtures/'
        shutil.copytree(fixtures_dir + fixture_name, project_dir)
