from dockerized.core.commands.dockercomposecommand import DockerComposeCommand


class PushCommand(DockerComposeCommand):
    def __init__(self, env=None, docker_compose=None):
        super().__init__(env, docker_compose)

    def run(self):
        return self.docker_compose.push()
