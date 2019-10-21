import pytest
from click.testing import CliRunner

from redash.cli import Context
from redash.editor import Editor


class MockEditor(Editor):
    def __init__(self, path):
        super().__init__(None, path=path)
        self.opened = False

    def open(self):
        self.opened = True


@pytest.fixture
def mock_editor(sql_file):
    return MockEditor(sql_file)


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def cli(cli_runner, mock_editor):
    def invoke(command, args, client=None, editor=mock_editor):
        editor.client = client
        return cli_runner.invoke(command, args, obj=Context(client, mock_editor))

    return invoke
