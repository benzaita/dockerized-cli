from dockerized.core.commands.dockercomposecommand import DockerComposeCommand


class ShellCommand(DockerComposeCommand):
    def __init__(self, env=None, docker_compose=None):
        super().__init__(env, docker_compose)

    def run(self):
        working_dir = self.env.get_working_dir()
        return self.docker_compose.run(working_dir=working_dir, command='/bin/sh')
