from datetime import timedelta

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


@responses.activate
def test_poll_until_success(client):
    job_id = 1

    responses.add(
        responses.GET,
        client.url(f"jobs/{job_id}"),
        status=200,
        json=dict(job=dict(status=1)),
    )
    responses.add(
        responses.GET,
        client.url(f"jobs/{job_id}"),
        status=200,
        json=dict(job=dict(status=3)),
    )
    responses.add(
        responses.GET,
        client.url(f"jobs/{job_id}"),
        status=200,
        json=dict(job=dict(status="Not Called")),
    )

    response = client.poll(f"jobs/{job_id}", sleep=0)

    assert response.get("job").get("status") == 3
    assert len(responses.calls) == 2
    assert not responses.assert_all_requests_are_fired


@responses.activate
def test_poll_until_failure(client):
    job_id = 1
    responses.add(
        responses.GET,
        client.url(f"jobs/{job_id}"),
        status=200,
        json=dict(job=dict(status=1)),
    )
    responses.add(
        responses.GET,
        client.url(f"jobs/{job_id}"),
        status=200,
        json=dict(job=dict(status=4)),
    )
    responses.add(
        responses.GET,
        client.url(f"jobs/{job_id}"),
        status=200,
        json=dict(job=dict(status="Never Called")),
    )

    response = client.poll(f"jobs/{job_id}", sleep=0)

    assert response.get("job").get("status") == 4
    assert len(responses.calls) == 2
    assert not responses.assert_all_requests_are_fired


@responses.activate
def test_poll_until_timeout(client):
    job_id = 1

    responses.add(
        responses.GET,
        client.url(f"jobs/{job_id}"),
        status=200,
        json=dict(job=dict(status="Make this request")),
    )

    responses.add(
        responses.GET,
        client.url(f"jobs/{job_id}"),
        status=200,
        json=dict(job=dict(status="Timeout before this request")),
    )

    response = client.poll(f"jobs/{job_id}", timeout=timedelta(seconds=0))

    assert response.get("job").get("status") == "Make this request"
    assert len(responses.calls) == 1
    assert not responses.assert_all_requests_are_fired
