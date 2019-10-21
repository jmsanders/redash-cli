from redash.commands.edit import edit


def test_edit_query(cli, mock_client):
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
    result = cli(edit, ["--query-id", query_id, "--query", "select 1"], client=client)

    assert not result.exception
    assert download_response in result.stdout
    assert (
        client.called_endpoint == f"queries/{query_id}/results/{query_result_id}.json"
    )


def test_edit_query_skip_execution(cli, mock_client):
    query_id = 12345
    expected = "result"
    client = mock_client(expected)
    result = cli(
        edit,
        ["--query-id", query_id, "--query", "select 1", "--execute", False],
        client=client,
    )

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == f"queries/{query_id}"
