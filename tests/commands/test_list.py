import pytest

import json
import requests
import responses

from redash.commands.list import list_


class MockClient:
    def __init__(self, return_value):
        self.return_value = return_value

    def get(self, endpoint, limit=None):
        self.called_endpoint = endpoint
        return self.return_value


def test_list_queries(cli_runner):
    expected = "result"
    result = cli_runner.invoke(list_, ["queries"], obj=MockClient(expected))

    assert not result.exception
    assert expected in result.stdout


def test_list_queries_with_limit(cli_runner):
    expected = "result"
    result = cli_runner.invoke(
        list_, ["queries", "--limit", 1], obj=MockClient(expected)
    )

    assert not result.exception
    assert expected in result.stdout


def test_list_my_queries(cli_runner):
    expected = "result"
    client = MockClient(expected)
    result = cli_runner.invoke(list_, ["queries", "--mine", True], obj=client)

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == "queries/my"


def test_list_my_queries_by_default(cli_runner):
    expected = "result"
    client = MockClient(expected)
    result = cli_runner.invoke(list_, ["queries"], obj=client)

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == "queries/my"


def test_list_everybodys_queries(cli_runner):
    expected = "result"
    client = MockClient(expected)
    result = cli_runner.invoke(list_, ["queries", "--mine", False], obj=client)

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == "queries"


def test_list_data_sources(cli_runner):
    expected = "result"
    result = cli_runner.invoke(list_, ["data-sources"], obj=MockClient(expected))

    assert not result.exception
    assert expected in result.stdout
