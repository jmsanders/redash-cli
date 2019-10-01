import pytest

import json
import requests
import responses

from redash.commands.list import list_


class MockClient:
    def __init__(self, return_value):
        self.return_value = return_value

    def get(self, endpoint, limit):
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
