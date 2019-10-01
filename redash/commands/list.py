import json

import click


@click.group(name="list", help="List a Redash object.")
@click.pass_obj
def list_(client):
    pass


@list_.command(help="List your queries.")
@click.option("--limit", type=int, default=25, help="Maximum number of results.")
@click.pass_obj
def queries(client, limit):
    print(json.dumps((client.get("queries/my", limit=limit))))
