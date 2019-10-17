import pytest
from click.testing import CliRunner


class MockClient:
    def __init__(self, return_value):
        self.return_value = return_value

    def get(self, endpoint, limit=None):
        self.called_endpoint = endpoint
        return self.return_value


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def mock_client():
    def mock_client_factory(return_value):
        return MockClient(return_value)

    return mock_client_factory
