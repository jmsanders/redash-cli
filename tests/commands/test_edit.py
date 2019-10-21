from redash.commands.edit import edit


def test_edit_query(cli_runner, mock_client):
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
    result = cli_runner.invoke(
        edit, ["--query-id", query_id, "--query", "select 1"], obj=client
    )

    assert not result.exception
    assert download_response in result.stdout
    assert (
        client.called_endpoint == f"queries/{query_id}/results/{query_result_id}.json"
    )


def test_edit_query_skip_execution(cli_runner, mock_client):
    query_id = 12345
    expected = "result"
    client = mock_client(expected)
    result = cli_runner.invoke(
        edit,
        ["--query-id", query_id, "--query", "select 1", "--execute", False],
        obj=client,
    )

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == f"queries/{query_id}"


def test_edit_query_edits_last_query(cli_runner, mock_client):
    query_id = 12345
    list_queries_response = [dict(id=query_id)]
    expected = "result"

    client = mock_client([list_queries_response, expected])
    result = cli_runner.invoke(
        edit, ["--query", "select 1", "--execute", False], obj=client
    )

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == f"queries/{query_id}"
