import click

from redash import utils


@click.command(help="Execute a query and get the results.")
@click.option("--query-id", type=int, help="ID of query to execute.")
@click.pass_obj
def download(client, query_id):
    if not query_id:
        query_id = client.get("queries/my", limit=1)[0].get("id")
    utils.echo(perform_download(client, query_id))


def perform_download(client, query_id):
    job_id = client.post(f"queries/{query_id}/refresh").get("job").get("id")
    query_result_id = client.poll(f"jobs/{job_id}").get("job").get("query_result_id")
    return client.get(f"queries/{query_id}/results/{query_result_id}.json")
