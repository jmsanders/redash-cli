import click


@click.group(help="Configure options.")
@click.pass_obj
def configure(context):
    pass


@configure.command(
    short_help="Your API key. Find this at https://app.redash.io/{organization}/users/me."
)
@click.argument("key")
@click.pass_obj
def api_key(context, key):
    context.client.config.set("api_key", key)


@configure.command(help="Your organization's Redash address.")
@click.argument("organization")
@click.pass_obj
def organization(context, organization):
    context.client.config.set("organization", organization)
