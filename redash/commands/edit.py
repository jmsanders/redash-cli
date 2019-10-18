import json

import click


@click.command(help="Edit and resubmit an existing query.")
@click.option("--query-id", type=int, required=True, help="ID of query to edit.")
@click.option("--query", type=str, required=True, help="SQL query string.")
@click.pass_obj
def edit(client, query_id, query):
    print(json.dumps(client.post(f"queries/{query_id}", dict(query=query))))
