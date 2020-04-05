class DockerClient:
    def run(self, stdout, command):
        stdout.write('something')
        return 42
