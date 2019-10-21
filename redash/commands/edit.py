import json

import click

from redash.commands.download import perform_download


def edit_query(editor, query_id):
    editor.save_query_to_file(query_id)
    editor.open()
    return editor.read_query_from_file()


@click.command(help="Edit and resubmit an existing query.")
@click.option("--query", type=str, help="SQL query string.")
@click.option("--query-id", type=int, required=True, help="ID of query to edit.")
@click.option(
    "--execute",
    type=bool,
    default=True,
    help="Execute the query and download its results.",
    show_default=True,
)
@click.pass_obj
def edit(context, query_id, query, execute):
    if not query:
        query = edit_query(context.editor, query_id)
    response = context.client.post(f"queries/{query_id}", dict(query=query))
    if execute:
        print(json.dumps(perform_download(context.client, query_id)))
    else:
        print(json.dumps(response))
