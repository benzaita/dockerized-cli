class DockerClient:
    def run(self, stdout, stderr, command):
        stdout.write('something out')
        stderr.write('something err')
        return 42
