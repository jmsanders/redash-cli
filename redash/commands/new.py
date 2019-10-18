import json

import click

DEFAULT_QUERY_NAME = "New redash-cli Query"


@click.command(help="Submit a new query.")
@click.option("--query", type=str, required=True, help="SQL query string.")
@click.option("--data-source-id", type=int, required=True, help="Data Source ID.")
@click.option(
    "--name",
    type=str,
    default=DEFAULT_QUERY_NAME,
    help="Query name.",
    show_default=True,
)
@click.pass_obj
def new(client, query, data_source_id, name):
    print(
        json.dumps(
            client.post(
                "queries", dict(query=query, data_source_id=data_source_id, name=name)
            )
        )
    )
