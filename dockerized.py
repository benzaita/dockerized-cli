#!/usr/bin/env python3

import click
from pathlib import Path
from commands.init import InitCommand, InitError


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


if __name__ == '__main__':
    cli()
