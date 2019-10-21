import json

import click


@click.command(help="Execute a query and get the results.")
@click.option("--query-id", type=int, required=True, help="ID of query to execute.")
@click.pass_obj
def download(context, query_id):
    print(json.dumps(perform_download(context.client, query_id)))


def perform_download(client, query_id):
    job_id = client.post(f"queries/{query_id}/refresh").get("job").get("id")
    query_result_id = client.poll(f"jobs/{job_id}").get("job").get("query_result_id")
    return client.get(f"queries/{query_id}/results/{query_result_id}.json")
