import pytest
from click.testing import CliRunner


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
def cli_runner():
    return CliRunner()


@pytest.fixture
def mock_client():
    def mock_client_factory(return_value):
        return MockClient(return_value)

    return mock_client_factory
