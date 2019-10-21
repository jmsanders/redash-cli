import json

import pytest

from redash.commands.new import new, DEFAULT_QUERY_NAME


def test_new_query(cli, mock_client):
    query_id = 12345
    expected_new_query_response = dict(id=query_id)
    job_id_response = dict(job=dict(id=1))
    query_result_id = 1
    query_result_id_response = dict(job=dict(query_result_id=query_result_id))
    download_response = "Success"

    client = mock_client(
        [
            expected_new_query_response,
            job_id_response,
            query_result_id_response,
            download_response,
        ]
    )
    result = cli(new, ["--query", "select 1", "--data-source-id", 1], client=client)

    assert not result.exception
    assert download_response in result.stdout
    assert (
        client.called_endpoint == f"queries/{query_id}/results/{query_result_id}.json"
    )


def test_new_query_with_skip_execution(cli, mock_client):
    query_id = 12345
    expected_new_query_response = dict(id=query_id)

    client = mock_client([expected_new_query_response])
    result = cli(
        new,
        ["--query", "select 1", "--data-source-id", 1, "--execute", False],
        client=client,
    )

    assert not result.exception
    assert json.dumps(expected_new_query_response) in result.stdout
    assert "results" not in client.called_endpoint


def test_new_query_without_name_provides_name(cli, mock_client):
    expected = dict(id=12345)
    client = mock_client(expected)
    result = cli(
        new,
        ["--query", "select 1", "--data-source-id", 1, "--execute", False],
        client=client,
    )

    assert not result.exception
    assert json.dumps(expected) in result.stdout
    assert client.recorded_payload.get("name") == DEFAULT_QUERY_NAME


def test_new_query_with_name(cli, mock_client):
    expected_result = dict(id=12345)
    expected_name = "Custom redash-cli query name"
    client = mock_client(expected_result)
    result = cli(
        new,
        [
            "--query",
            "select 1",
            "--data-source-id",
            1,
            "--name",
            expected_name,
            "--execute",
            False,
        ],
        client=client,
    )

    assert not result.exception
    assert json.dumps(expected_result) in result.stdout
    assert client.recorded_payload.get("name") == expected_name


def test_new_without_query_opens_empty_editor(cli, mock_client, mock_editor, sql_file):
    expected = dict(id=1)
    client = mock_client(expected)

    assert not mock_editor.opened
    with pytest.raises(Exception):
        open(sql_file)

    result = cli(new, ["--data-source-id", 1, "--execute", False], client=client)

    assert not result.exception
    assert json.dumps(expected) in result.stdout
    assert mock_editor.opened
    assert mock_editor.read_query_from_file() == ""
