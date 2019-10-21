import subprocess

import pytest

from redash.editor import Editor

@pytest.fixture
def sql_file(tmp_path):
    return tmp_path / "redash-cli.sql"

@pytest.fixture
def editor(sql_file):
    return Editor(sql_file)


def test_save_query_to_file(editor, mock_client, sql_file):
    query = "select 1"
    response = dict(query=query)
    client = mock_client(response)

    with pytest.raises(Exception):
        open(sql_file)

    editor.save_query_to_file(client, 12345)

    with open(sql_file, "r") as f:
        assert query == f.read()

def test_read_query_from_file(editor, sql_file):
    assert not editor.read_query_from_file()

    query = "select 1"
    with open(sql_file, "w") as f:
        f.write(query)

    assert editor.read_query_from_file() == query


def test_open(editor, sql_file, mocker):
    mocker.patch("subprocess.call")

    editor.open()

    subprocess.call.assert_called_once_with([editor.editor, sql_file])