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
