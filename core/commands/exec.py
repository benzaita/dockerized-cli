from adapters.dockercompose import DockerCompose
from adapters.environment import Environment


class ExecCommand:
    command: str

    def __init__(self, command):
        self.command = command
        self.env = Environment()

    def run(self):
        docker_compose = DockerCompose()
        working_dir = self.env.get_working_dir()
        project_dir = self.env.get_project_dir()
        return docker_compose.run(
            composefile=project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            working_dir=working_dir,
            bind_dir=working_dir,
            command=self.command
        )
