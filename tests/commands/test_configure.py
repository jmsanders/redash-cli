from redash.commands.configure import configure


def test_set_api_key(cli, client):
    api_key = "my_api_key"
    result = cli(configure, ["api-key", api_key], client=client)
    assert not result.exception
    assert client.config.api_key == api_key


def test_set_organization(cli, client):
    organization = "my organization"
    result = cli(configure, ["organization", organization], client=client)
    assert not result.exception
    assert client.config.organization == organization
