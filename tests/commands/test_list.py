from redash.commands.list import list_


def test_list_queries(cli, mock_client):
    expected = "result"
    result = cli(list_, ["queries"], client=mock_client(expected))

    assert not result.exception
    assert expected in result.stdout


def test_list_queries_with_limit(cli, mock_client):
    expected = "result"
    result = cli(list_, ["queries", "--limit", 1], client=mock_client(expected))

    assert not result.exception
    assert expected in result.stdout


def test_list_my_queries(cli, mock_client):
    expected = "result"
    client = mock_client(expected)
    result = cli(list_, ["queries", "--mine", True], client=client)

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == "queries/my"


def test_list_my_queries_by_default(cli, mock_client):
    expected = "result"
    client = mock_client(expected)
    result = cli(list_, ["queries"], client=client)

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == "queries/my"


def test_list_everybodys_queries(cli, mock_client):
    expected = "result"
    client = mock_client(expected)
    result = cli(list_, ["queries", "--mine", False], client=client)

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == "queries"


def test_list_data_sources(cli, mock_client):
    expected = "result"
    result = cli(list_, ["data-sources"], client=mock_client(expected))

    assert not result.exception
    assert expected in result.stdout
