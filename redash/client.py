import os

import requests


class RedashClient:
    def __init__(self, config):
        self.config = config

    @property
    def base_url(self):
        return os.path.join("https://redash.io", self.config.organization, "api")

    @property
    def headers(self):
        return dict(Authorization=f"Key {self.config.api_key}")

    def url(self, url_part):
        return os.path.join(self.base_url, url_part)

    def get(self, url_part):
        response = requests.get(
            self.url(url_part), headers=self.headers, allow_redirects=False
        )
        if response.is_redirect or not response.ok:
            raise Exception()
        return response.json()

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
