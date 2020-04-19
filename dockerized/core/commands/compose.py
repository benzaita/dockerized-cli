from dockerized.core.commands.dockercomposecommand import DockerComposeCommand


class ComposeCommand(DockerComposeCommand):
    def __init__(self, args, env=None, docker_compose=None):
        super().__init__(env, docker_compose)
        self.args = args

    def run(self):
        return self.docker_compose.execute_command(self.args)
