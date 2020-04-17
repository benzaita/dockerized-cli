from dockerized.core.commands.dockercomposecommand import DockerComposeCommand


class CleanCommand(DockerComposeCommand):
    def __init__(self):
        super().__init__()

    def run(self):
        return self.docker_compose.down()
