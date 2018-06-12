import requests
from urllib.parse import urlencode

from .conf import (
    PIPEDRIVE_URL,
    PIPEDRIVE_API_KEY,
    SEARCH_URL,
)


class PDBase:
    PIPEDRIVE_URL = PIPEDRIVE_URL
    PIPEDRIVE_API_KEY = PIPEDRIVE_API_KEY
    SEARCH_URL = SEARCH_URL

    def __init__(self, api_key=None, api_url=None):
        self.api_key = api_key or self.PIPEDRIVE_API_KEY
        self.api_url = api_url or self.PIPEDRIVE_URL

    def _request(self, method, *args, **kwargs):
        METHODS = {'GET': requests.get, 'POST': requests.post}
        try:
            response = METHODS[method](*args, **kwargs)
        except requests.exceptions.ConnectionError:
            raise ConnectionError('We cannot connect with PipeDrive')

        data = response.json()
        if not response.ok:
            raise ConnectionError(data.get('error', ''))

        return data

    def url(self, endpoint, query_string=None):
        qs = dict(api_token=self.api_key)
        qs.update(query_string or {})
        return f'{self.api_url}{endpoint}?{urlencode(qs)}'

    def generic_search(self, term, item_type):
        url = self.url(self.SEARCH_URL, dict(item_type=item_type, term=term))
        return self._request(requests.get, url)
