from redash.commands.download import download


def test_download(cli, mock_client):
    job_id_response = dict(job=dict(id=1))
    query_result_id_response = dict(job=dict(query_result_id=1))
    download_response = "Success"
    client = mock_client([job_id_response, query_result_id_response, download_response])

    result = cli(download, ["--query-id", 12345], client=client)

    assert not result.exception
    assert download_response in result.stdout
    assert client.called_endpoint == "queries/12345/results/1.json"
