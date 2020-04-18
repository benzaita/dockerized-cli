from dockerized.core.commands.dockercomposecommand import DockerComposeCommand


class CleanCommand(DockerComposeCommand):
    def __init__(self):
        super().__init__()

    def run(self):
        self.docker_compose.down()
        self.set_project_prepared(False)
