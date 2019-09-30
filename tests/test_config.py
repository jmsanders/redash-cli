import pytest

from configparser import ConfigParser
import os

from redash.config import Config


@pytest.fixture
def config_path(tmp_path):
    return tmp_path / "config.INI"


@pytest.fixture
def config(config_path):
    return Config(config_path)


def test_init_loads_existing_configuration(config_path):
    existing_config = ConfigParser()
    existing_config["DEFAULT"]["configured"] = "yes"

    with open(config_path, "w") as f:
        existing_config.write(f)

    new_config = Config(config_path)
    assert new_config.config["DEFAULT"]["configured"]


def test_init_does_not_raise_if_no_existing_configuration(config_path):
    config = Config(config_path)
    assert config.config


def test_persist_creates_a_config_file_if_not_exists(config):
    assert not os.path.exists(config.path)

    config.persist()

    assert os.path.exists(config.path)


def test_persist_overwrites_a_config_file_if_it_already_exists(config):
    existing = "existing config"
    with open(config.path, "w") as f:
        f.write(existing)

    with open(config.path, "r") as f:
        assert existing in f.read()

    config.persist()

    with open(config.path, "r") as f:
        assert existing not in f.read()


def test_set_persists_a_new_default_configuration(config):
    config.set("configured", "yes")

    with open(config.path, "r") as f:
        assert "yes" in f.read()


def test_set_persists_over_an_existing_default_configuration(config_path):
    existing_config = ConfigParser()
    existing_config["DEFAULT"]["configured"] = "no"

    config = Config(config_path)
    config.set("configured", "yes")

    with open(config_path, "r") as f:
        assert "yes" in f.read()


def test_get_gets_from_the_default_configuration(config):
    config.config["DEFAULT"]["configured"] = "yes"
    config.config["other"] = {}
    config.config["other"]["configured"] = "no"

    assert config.get("configured") == "yes"
