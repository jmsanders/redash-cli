import click

from redash import utils
from redash.commands.download import perform_download


@click.command(help="Edit and resubmit an existing query.")
@click.option("--query-id", type=int, help="ID of query to edit.")
@click.option("--query", type=str, help="SQL query string.")
@click.option(
    "--execute",
    type=bool,
    default=True,
    help="Execute the query and download its results.",
    show_default=True,
)
@click.pass_obj
def edit(client, query_id, query, execute):
    if not query_id:
        query_id = client.get("queries/my", limit=1)[0].get("id")
    if not query:
        initial_query = client.get(f"queries/{query_id}").get("query")
        query = click.edit(text=initial_query, extension=".sql")
    response = client.post(f"queries/{query_id}", dict(query=query))
    if execute:
        utils.echo(perform_download(client, query_id))
    else:
        utils.echo(response)
