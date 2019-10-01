import pytest

import responses


@responses.activate
def test_get_returns_response_body(client):
    body = "Response Body"
    responses.add(
        responses.GET, client.url("queries"), headers=client.headers, json=body
    )

    response = client.get("queries")
    assert response == body


@responses.activate
def test_get_raises_for_status(client):
    responses.add(responses.GET, client.url("queries"), status=404)

    with pytest.raises(Exception):
        client.get("queries")


@responses.activate
def test_get_raises_for_redirects(client):
    responses.add(responses.GET, client.url("queries"), status=302)

    with pytest.raises(Exception):
        client.get("queries")


@responses.activate
def test_get_with_params(client):
    body = "Response Body"
    params = dict(page_size=2)
    responses.add(
        responses.GET, client.url("queries?page_size=2"), status=200, json=body
    )

    response = client.get("queries", params=params)
    assert response == body


@responses.activate
def test_get_gets_all_paginated_responses(client):
    responses.add(
        responses.GET,
        client.url("queries"),
        status=200,
        json=dict(count=2, page=1, page_size=1, results=[1]),
    )
    responses.add(
        responses.GET,
        client.url("queries"),
        status=200,
        json=dict(count=2, page=2, page_size=1, results=[2]),
    )

    response = client.get("queries")
    assert response == [1, 2]


@responses.activate
def test_get_can_limit_the_number_of_results(client):
    responses.add(
        responses.GET,
        client.url("queries"),
        status=200,
        json=dict(count=3, page=1, page_size=2, results=[1, 2]),
    )
    responses.add(
        responses.GET,
        client.url("queries"),
        status=200,
        json=dict(count=3, page=2, page_size=2, results=[3]),
    )

    response = client.get("queries", limit=1)
    assert response == [1]


@responses.activate
def test_post_returns_response_body(client):
    body = "Response Body"
    responses.add(
        responses.POST, client.url("queries"), headers=client.headers, json=body
    )

    response = client.post("queries")
    assert response == body


@responses.activate
def test_post_raises_for_status(client):
    responses.add(responses.POST, client.url("queries"), status=404)

    with pytest.raises(Exception):
        client.post("queries")


@responses.activate
def test_post_raises_for_redirects(client):
    responses.add(responses.POST, client.url("queries"), status=302)

    with pytest.raises(Exception):
        client.post("queries")
