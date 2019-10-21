import click

from redash import utils


@click.group(name="list", help="List a Redash object.")
@click.pass_obj
def list_(client):
    pass


@list_.command(help="List data sources.")
@click.pass_obj
def data_sources(client):
    utils.echo(client.get("data_sources"))


@list_.command(help="List your queries.")
@click.option(
    "--limit",
    type=int,
    default=25,
    help="Maximum number of results.",
    show_default=True,
)
@click.option(
    "--mine", type=bool, default=True, help="Return only my queries.", show_default=True
)
@click.pass_obj
def queries(client, limit, mine):
    endpoint = "queries/my" if mine else "queries"
    utils.echo(client.get(endpoint, limit=limit))
