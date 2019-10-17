import pytest

import json
import requests
import responses

from redash.commands.new import new, DEFAULT_QUERY_NAME


def test_new_query_without_name_provides_name(cli_runner, mock_client):
    expected = "result"
    client = mock_client(expected)
    result = cli_runner.invoke(
        new, ["--query", "select 1", "--data-source-id", 1], obj=client
    )

    assert not result.exception
    assert expected in result.stdout
    assert client.recorded_payload.get("name") == DEFAULT_QUERY_NAME


def test_new_query_with_name(cli_runner, mock_client):
    expected_result = "result"
    expected_name = "Custom redash-cli query name"
    client = mock_client(expected_result)
    result = cli_runner.invoke(
        new,
        ["--query", "select 1", "--data-source-id", 1, "--name", expected_name],
        obj=client,
    )

    assert not result.exception
    assert expected_result in result.stdout
    assert client.recorded_payload.get("name") == expected_name
