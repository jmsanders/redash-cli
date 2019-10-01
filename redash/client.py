import os

import requests


class RedashClient:
    def __init__(self, config):
        self.config = config

    @property
    def base_url(self):
        return os.path.join("https://app.redash.io", self.config.organization, "api")

    @property
    def headers(self):
        return dict(Authorization=f"Key {self.config.api_key}")

    def url(self, url_part):
        return os.path.join(self.base_url, url_part)

    def get(self, url_part, params=None):
        paginate = True
        results = []
        while paginate:
            response = requests.get(
                self.url(url_part),
                headers=self.headers,
                params=params,
                allow_redirects=False,
            )
            if response.is_redirect or not response.ok:
                raise Exception()
            payload = response.json()
            if self._is_paginated_response(payload):
                results += payload.get("results")
                paginate = self._has_more_pages(payload)
            else:
                return payload
        return results

    def _has_more_pages(self, payload):
        return payload.get("page") * payload.get("page_size") < payload.get("count")

    def _is_paginated_response(self, payload):
        return isinstance(payload, dict) and payload.get("results")

    def post(self, url_part, payload=None):
        response = requests.post(
            self.url(url_part),
            headers=self.headers,
            allow_redirects=False,
            json=payload,
        )
        if response.is_redirect or not response.ok:
            raise Exception()
        return response.json()
