import click

from redash import utils
from redash.commands.download import perform_download

DEFAULT_QUERY_NAME = "New redash-cli Query"


@click.command(help="Submit a new query.")
@click.option("--query", type=str, help="SQL query string.")
@click.option("--data-source-id", type=int, required=True, help="Data Source ID.")
@click.option(
    "--name",
    type=str,
    default=DEFAULT_QUERY_NAME,
    help="Query name.",
    show_default=True,
)
@click.option(
    "--execute",
    type=bool,
    default=True,
    help="Execute the query and download its results.",
    show_default=True,
)
@click.pass_obj
def new(client, query, data_source_id, name, execute):
    if not query:
        query = click.edit(extension=".sql")
    response = client.post(
        "queries", dict(query=query, data_source_id=data_source_id, name=name)
    )
    query_id = response.get("id")
    if execute:
        utils.echo(perform_download(client, query_id))
    else:
        utils.echo(response)
