import logging
import time
from dockerized.core.commands.dockercomposecommand import DockerComposeCommand

logger = logging.getLogger(__name__)


class ExecCommand(DockerComposeCommand):
    command: str

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.lockpath = self.project_dir.joinpath('.dockerized').joinpath('lock')

    def run(self):
        self.__ensure_prepared()

        working_dir = self.env.get_working_dir()
        return self.docker_compose.run(working_dir=working_dir, command=self.command)

    def __ensure_prepared(self):
        # Ensure the Docker-Compose resources are requested only once, when parallel invocations of "exec" are
        # happening.
        # Otherwise, when running in a pristine project (where Docker-Compose did not create a Docker network, for
        # example) the parallel invocations trigger parallel requests to create Docker resources which may conflict.
        while not self.is_project_prepared():
            logger.info(f"Trying to lock {self.lockpath}")
            if self.__try_lock():
                try:
                    logger.info(f"Preparing {self.project_dir}")
                    self.__prepare()
                finally:
                    logger.info(f"Unlocking {self.lockpath}")
                    self.__unlock()
            else:
                retry_interval_secs = 1
                logger.info(f"Locking failed, retrying in {retry_interval_secs} secs")
                time.sleep(retry_interval_secs)
        logger.info(f"{self.project_dir} is prepared")

    def __try_lock(self):
        try:
            self.lockpath.mkdir()
            return True
        except OSError:
            if self.lockpath.is_dir():
                return False
            else:
                raise

    def __unlock(self):
        self.lockpath.rmdir()

    def __prepare(self):
        self.docker_compose.run(working_dir=self.project_dir, command='true')
        self.set_project_prepared(True)

