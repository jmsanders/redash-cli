import pytest

from redash.config import Config
from redash.client import RedashClient


class MockClient:
    def __init__(self, return_values):
        self.return_values = (
            return_values if isinstance(return_values, list) else [return_values]
        )

    def get(self, endpoint, limit=None):
        self.called_endpoint = endpoint
        return self.return_values.pop(0)

    def post(self, endpoint, payload=None):
        self.called_endpoint = endpoint
        self.recorded_payload = payload
        return self.return_values.pop(0)

    def poll(self, endpoint):
        self.called_endpoint = endpoint
        return self.return_values.pop(0)


@pytest.fixture
def config(tmp_path):
    config = Config(tmp_path / "config.ini")
    config.set("api_key", "abc123")
    config.set("organization", "organization")
    return config


@pytest.fixture
def client(config):
    return RedashClient(config)


@pytest.fixture
def mock_client():
    def mock_client_factory(return_values=None):
        return MockClient(return_values)

    return mock_client_factory


@pytest.fixture
def sql_file(tmp_path):
    return tmp_path / "redash-cli.sql"
