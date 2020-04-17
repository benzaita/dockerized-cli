from dockerized.core.commands.dockercomposecommand import DockerComposeCommand


class ExecCommand(DockerComposeCommand):
    command: str

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        working_dir = self.env.get_working_dir()
        return self.docker_compose.run(working_dir=working_dir, command=self.command)
