import click
import json


def echo(content):
    click.echo_via_pager(json.dumps(content, indent=4))
