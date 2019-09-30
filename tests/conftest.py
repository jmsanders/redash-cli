import pytest

from redash.config import Config
from redash.client import RedashClient


@pytest.fixture
def config(tmp_path):
    config = Config(tmp_path / "config.ini")
    config.set("api_key", "abc123")
    config.set("organization", "organization")
    return config


@pytest.fixture
def client(config):
    return RedashClient(config)
