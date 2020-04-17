from pathlib import Path

import click

from core.commands.compose import ComposeCommand
from core.commands.shell import ShellCommand
from core.commands.clean import CleanCommand
from core.commands.init import InitCommand
from core.commands.exec import ExecCommand
from core.commands.errors import CommandError

from contextlib import contextmanager


@contextmanager
def friendly_dockerized_errors(click):
    try:
        yield
    except CommandError as err:
        click.echo(err.message, err=True)
        click.get_current_context().exit(1)


@click.group()
def main():
    pass


@main.command()
def init():
    with friendly_dockerized_errors(click):
        init_command = InitCommand(Path.cwd())
        init_command.run()
    click.echo('created')


@main.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def exec(command):
    exit_code = 0
    with friendly_dockerized_errors(click):
        exec_command = ExecCommand(' '.join(command))
        exit_code = exec_command.run()
    click.get_current_context().exit(exit_code)


@main.command()
def clean():
    with friendly_dockerized_errors(click):
        clean_command = CleanCommand()
        clean_command.run()


@main.command()
def shell():
    exit_code = 0
    with friendly_dockerized_errors(click):
        shell_command = ShellCommand()
        exit_code = shell_command.run()
    click.get_current_context().exit(exit_code)


@main.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def compose(command):
    exit_code = 0
    with friendly_dockerized_errors(click):
        compose_command = ComposeCommand(command)
        exit_code = compose_command.run()
    click.get_current_context().exit(exit_code)
