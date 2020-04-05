#!/usr/bin/env python3

import click
from pathlib import Path
from commands.init import InitCommand, InitError
from commands.exec import ExecCommand


@click.group()
def cli():
    pass


@cli.command()
def init():
    init_command = InitCommand(Path.cwd())
    try:
        init_command.run()
    except InitError as err:
        click.echo(err.message, err=True)
        click.get_current_context().exit(1)
    click.echo('created')


@cli.command()
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def exec(command):
    stdout = click.get_text_stream('stdout')
    stderr = click.get_text_stream('stderr')
    exec_command = ExecCommand(Path.cwd(), stdout, stderr, command)
    exit_code = exec_command.run()
    stderr.flush()
    click.get_current_context().exit(exit_code)


if __name__ == '__main__':
    cli()
