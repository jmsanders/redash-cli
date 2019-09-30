import pytest

from redash.commands.configure import configure


def test_set_api_key(cli_runner, client):
    api_key = "my_api_key"
    result = cli_runner.invoke(configure, ["api-key", api_key], obj=client)
    assert not result.exception
    assert client.config.api_key == api_key


def test_set_organization(cli_runner, client):
    organization = "my organization"
    result = cli_runner.invoke(configure, ["organization", organization], obj=client)
    assert not result.exception
    assert client.config.organization == organization
