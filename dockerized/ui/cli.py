import logging
from pathlib import Path

import click

from dockerized.core.commands.push import PushCommand
from dockerized.core.commands.version import VersionCommand
from dockerized.core.commands.compose import ComposeCommand
from dockerized.core.commands.shell import ShellCommand
from dockerized.core.commands.clean import CleanCommand
from dockerized.core.commands.init import InitCommand
from dockerized.core.commands.exec import ExecCommand
from dockerized.core.commands.errors import CommandError

from contextlib import contextmanager


@contextmanager
def friendly_dockerized_errors(click):
    try:
        yield
    except CommandError as err:
        click.echo(err.message, err=True)
        click.get_current_context().exit(1)


@click.group()
@click.option(
    '--loglevel',
    default='WARNING',
    type=click.Choice(
        map(logging.getLevelName, [logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL, logging.DEBUG]),
        case_sensitive=True
    )
)
def main(loglevel):
    logging.basicConfig(level=loglevel)


@main.command(
    short_help='Initialize Dockerized in the current directory'
)
def init():
    with friendly_dockerized_errors(click):
        init_command = InitCommand(Path.cwd())
        init_command.run()
    click.echo('created')


@main.command(
    short_help='Execute a command in the container',
    help="""
    Execute COMMAND in the 'dockerized' container. The project directory (the 
    parent of the .dockerized/ directory), as well as the current working 
    directory are available to COMMAND. This means you can seamlessly run 
    commands like `ls -l` or `pwd` -- the will produce the same output in the
    container as in the host. Additionally, you can seamlessly run commands 
    which depend on tools that are available in the container, but not on the
    host.
    
    ## Passing environment variables
    
    To pass environment variables to the COMMAND, simply prepend it with them:
    
       dockerized exec FOO=123 env
    
    If you always pass the same environment variables to the container, you 
    can instead put them inside the `.dockerized/docker-compose.dockerized.yml`
    file under the `services.dockerized.environment` section. 
    """,
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def exec(command):
    exit_code = 0
    with friendly_dockerized_errors(click):
        exec_command = ExecCommand(' '.join(command))
        exit_code = exec_command.run()
    click.get_current_context().exit(exit_code)


@main.command(
    short_help='Clean the Docker resources used by this project'
)
def clean():
    exit_code = 0
    with friendly_dockerized_errors(click):
        clean_command = CleanCommand()
        exit_code = clean_command.run()
    click.get_current_context().exit(exit_code)


@main.command(
    short_help='Push the \'dockerized\' image'
)
def push():
    exit_code = 0
    with friendly_dockerized_errors(click):
        push_command = PushCommand()
        exit_code = push_command.run()
    click.get_current_context().exit(exit_code)


@main.command(
    short_help='Enter an interactive shell inside the container'
)
def shell():
    exit_code = 0
    with friendly_dockerized_errors(click):
        shell_command = ShellCommand()
        exit_code = shell_command.run()
    click.get_current_context().exit(exit_code)


@main.command(
    short_help='Run an arbitrary Docker-Compose command in this project',
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def compose(command):
    exit_code = 0
    with friendly_dockerized_errors(click):
        compose_command = ComposeCommand(command)
        exit_code = compose_command.run()
    click.get_current_context().exit(exit_code)


@main.command()
def version():
    version_command = VersionCommand()
    version = version_command.run()
    click.echo(version)