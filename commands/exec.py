from typing import List

from clients.docker import DockerClient


class ExecCommand:
    stdout: object
    command: List[str]

    def __init__(self, work_dir, stdout, stderr, command):
        self.command = command
        self.stdout = stdout
        pass

    def run(self):
        docker_client = DockerClient()
        return docker_client.run(self.stdout, self.command)
