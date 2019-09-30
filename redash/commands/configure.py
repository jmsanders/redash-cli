import click


@click.group(help="Configure options.")
@click.pass_obj
def configure(client):
    pass


@configure.command(
    short_help="Your API key. Find this at https://app.redash.io/{organization}/users/me."
)
@click.argument("key")
@click.pass_obj
def api_key(client, key):
    client.config.set("api_key", key)


@configure.command(help="Your organization's Redash address.")
@click.argument("organization")
@click.pass_obj
def organization(client, organization):
    client.config.set("organization", organization)
