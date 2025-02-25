from typing import Optional
from requests import Response
from pluggy_py.utils.http_client import HttpClient
from pluggy_py.models.identity import Identity

class IdentityResource:
    """
    IdentityResource handles the /identity endpoints:
      - GET /identity?itemId=...
      - GET /identity/{id}
    """

    def __init__(self, http_client: HttpClient, api_key: str):
        self._http = http_client
        self._api_key = api_key

    def find_by_item(self, item_id: str) -> Identity:
        """
        GET /identity?itemId={item_id}
        Recovers the identity of an item if available.
        """
        headers = {"X-API-KEY": self._api_key}
        params = {"itemId": item_id}
        response: Response = self._http.get("/identity", params=params, headers=headers)
        return Identity(**response.json())

    def retrieve_identity(self, identity_id: str) -> Identity:
        """
        GET /identity/{id}
        Recovers the identity resource by its id.
        """
        headers = {"X-API-KEY": self._api_key}
        response: Response = self._http.get(f"/identity/{identity_id}", headers=headers)
        return Identity(**response.json())
