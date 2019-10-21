import json

import click

from redash.commands.download import perform_download

DEFAULT_QUERY_NAME = "New redash-cli Query"


@click.pass_obj
def create_query(context):
    context.editor.reset()
    context.editor.open()
    return context.editor.read_query_from_file()


@click.command(help="Submit a new query.")
@click.option("--query", type=str, default=create_query, help="SQL query string.")
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
def new(context, query, data_source_id, name, execute):
    response = context.client.post(
        "queries", dict(query=query, data_source_id=data_source_id, name=name)
    )
    query_id = response.get("id")
    if execute:
        print(json.dumps(perform_download(context.client, query_id)))
    else:
        print(json.dumps(response))
