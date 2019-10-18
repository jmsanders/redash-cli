from redash.commands.edit import edit


def test_edit_query(cli_runner, mock_client):
    query_id = 12345
    expected = "result"
    client = mock_client(expected)
    result = cli_runner.invoke(
        edit, ["--query-id", query_id, "--query", "select 1"], obj=client
    )

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == f"queries/{query_id}"
