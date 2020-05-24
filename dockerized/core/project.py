import logging
import time

from dockerized.core.errors import DockerizedError

logger = logging.getLogger(__name__)


class Project:
    def __init__(self, project_dir, env, docker_compose):
        self.env = env
        self.docker_compose = docker_compose

        self.project_dir = project_dir
        self.prepared_flag_path = self.project_dir.joinpath('.dockerized').joinpath('prepared')
        self.lock_dir = self.project_dir.joinpath('.dockerized').joinpath('lock')

    def is_prepared(self):
        flag_exists = self.env.path_exists(self.prepared_flag_path)
        if flag_exists:
            flag_modification_time = self.env.get_file_modification_time(self.prepared_flag_path)

            composefile_path = self.project_dir.joinpath('.dockerized').joinpath('docker-compose.dockerized.yml')
            composefile_modification_time = self.env.get_file_modification_time(
                composefile_path)
            if composefile_modification_time > flag_modification_time:
                logger.info(f"{composefile_path} has changed since project was prepared")
                return False

            dockerfile_path = self.project_dir.joinpath('.dockerized').joinpath('Dockerfile.dockerized')
            if self.env.path_exists(dockerfile_path):
                dockerfile_modification_time = self.env.get_file_modification_time(
                    dockerfile_path)
                if dockerfile_modification_time > flag_modification_time:
                    logger.info(f"{dockerfile_path} has changed since project was prepared")
                    return False

            return True
        else:
            return False

    def set_prepared(self, state):
        if state:
            logger.info(f"Marking {self.project_dir} as 'already prepared'")
            self.env.touch_file(self.prepared_flag_path)
        else:
            logger.info(f"Marking {self.project_dir} as 'not prepared'")
            try:
                self.env.unlink_file(self.prepared_flag_path)
            except FileNotFoundError:
                pass

    def prepare_if_needed(self):
        # Ensure the Docker-Compose resources are requested only once, when parallel invocations of "exec" are
        # happening.
        # Otherwise, when running in a pristine project (where Docker-Compose did not create a Docker network, for
        # example) the parallel invocations trigger parallel requests to create Docker resources which may conflict.
        while not self.is_prepared():
            logger.info(f"Trying to lock {self.lock_dir}")
            if self.__try_lock():
                try:
                    logger.info(f"Preparing {self.project_dir}")
                    self.__prepare()
                    self.set_prepared(True)
                finally:
                    logger.info(f"Unlocking {self.lock_dir}")
                    self.__unlock()
            else:
                retry_interval_secs = 1
                logger.info(f"Locking failed, retrying in {retry_interval_secs} secs")
                time.sleep(retry_interval_secs)
        logger.info(f"{self.project_dir} is prepared")

    def __try_lock(self):
        try:
            self.env.mkdir(self.lock_dir)
            return True
        except OSError:
            if self.lock_dir.is_dir():
                return False
            else:
                raise

    def __unlock(self):
        self.env.rmdir(self.lock_dir)

    def __prepare(self):
        exit_code = self.docker_compose.pull()
        if exit_code != 0:
            logger.info(f"Pulling the 'dockerized' image exited with code {exit_code}. Ignoring error since we are "
                        f"going to build the image")

        # Explicitly running "build" because Docker Compose will not rebuild the image if it already exists, even if the
        # Dockerfile has changed since the image was built.
        exit_code = self.docker_compose.build()
        if exit_code != 0:
            raise DockerizedError("Failed to prepare: docker-compose build failed")

        # Running "run" because there is no other way (at the time of writing) to request Docker Compose to create the
        # network of that stack.
        self.docker_compose.run(working_dir=self.project_dir, command='true')
