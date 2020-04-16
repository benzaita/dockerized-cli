from adapters.dockercompose import DockerCompose
from adapters.environment import Environment


class CleanCommand:
    def __init__(self):
        self.env = Environment()

    def run(self):
        project_dir = self.env.get_project_dir()
        if project_dir is None:
            raise Exception("Not inside a Dockerized project directory. Did you run 'dockerized init'?")
        docker_compose = DockerCompose(
            composefile=project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml'),
            project_dir=project_dir
        )
        return docker_compose.clean()
