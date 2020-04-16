from adapters.dockercompose import DockerCompose
from adapters.environment import Environment


class ExecError(Exception):
    def __init__(self, message):
        self.message = message


class ExecCommand:
    command: str

    def __init__(self, command):
        self.command = command
        self.env = Environment()

    def run(self):
        project_dir = self.env.get_project_dir()
        if project_dir is None:
            raise ExecError("Not inside a Dockerized project directory. Did you run 'dockerized init'?")
        docker_compose = DockerCompose(
            composefile=project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            project_dir=project_dir
        )
        working_dir = self.env.get_working_dir()
        return docker_compose.run(
            working_dir=working_dir,
            command=self.command
        )
