import datetime
import os
import time

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

    def get(self, url_part, params=None, limit=None):
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
                paginate = self._keep_paginating(payload, limit)
            else:
                return payload
        return results[:limit]

    def _keep_paginating(self, payload, limit):
        return payload.get("page") * payload.get("page_size") < (
            limit or payload.get("count")
        )

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

    def poll(self, url_part, timeout=datetime.timedelta(minutes=1), sleep=1):
        start_time = datetime.datetime.now()
        response = self.get(url_part)

        while not self._is_finished(response.get("job")) and not self._is_timed_out(
            start_time, timeout
        ):
            time.sleep(sleep)
            response = self.get(url_part)

        return response

    def _is_finished(self, job):
        return job.get("status") in [3, 4]

    def _is_timed_out(self, start_time, timeout):
        return datetime.datetime.now() >= start_time + timeout
