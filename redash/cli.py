import os
import sys

import click

from redash.config import Config
from redash.client import RedashClient
from redash.commands.configure import configure
from redash.commands.list import list_


@click.group(help="Query Redash from your $EDITOR of choice.")
@click.pass_context
def cli(ctx):
    config = Config("config.ini")
    client = RedashClient(config)
    ctx.obj = client


cli.add_command(configure)
cli.add_command(list_)
