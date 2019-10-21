from redash.commands.list import list_


def test_list_queries(cli_runner, mock_client):
    expected = "result"
    result = cli_runner.invoke(list_, ["queries"], obj=mock_client(expected))

    assert not result.exception
    assert expected in result.stdout


def test_list_queries_with_limit(cli_runner, mock_client):
    expected = "result"
    result = cli_runner.invoke(
        list_, ["queries", "--limit", 1], obj=mock_client(expected)
    )

    assert not result.exception
    assert expected in result.stdout


def test_list_my_queries(cli_runner, mock_client):
    expected = "result"
    client = mock_client(expected)
    result = cli_runner.invoke(list_, ["queries", "--mine", True], obj=client)

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == "queries/my"


def test_list_my_queries_by_default(cli_runner, mock_client):
    expected = "result"
    client = mock_client(expected)
    result = cli_runner.invoke(list_, ["queries"], obj=client)

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == "queries/my"


def test_list_everybodys_queries(cli_runner, mock_client):
    expected = "result"
    client = mock_client(expected)
    result = cli_runner.invoke(list_, ["queries", "--mine", False], obj=client)

    assert not result.exception
    assert expected in result.stdout
    assert client.called_endpoint == "queries"


def test_list_data_sources(cli_runner, mock_client):
    expected = "result"
    result = cli_runner.invoke(list_, ["data-sources"], obj=mock_client(expected))

    assert not result.exception
    assert expected in result.stdout
