import os

import click

from redash.config import Config
from redash.client import RedashClient
from redash.commands.configure import configure
from redash.commands.download import download
from redash.commands.edit import edit
from redash.commands.list import list_
from redash.commands.new import new


@click.group(help="Query Redash from your $EDITOR of choice.")
@click.pass_context
def cli(ctx):
    config = Config(os.path.join(os.path.expanduser("~"), ".redash-cli.ini"))
    client = RedashClient(config)
    ctx.obj = client


cli.add_command(configure)
cli.add_command(download)
cli.add_command(edit)
cli.add_command(list_)
cli.add_command(new)
