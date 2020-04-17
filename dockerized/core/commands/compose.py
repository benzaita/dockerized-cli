from dockerized.core.commands.dockercomposecommand import DockerComposeCommand


class ComposeCommand(DockerComposeCommand):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def run(self):
        return self.docker_compose.execute_command(self.args)
