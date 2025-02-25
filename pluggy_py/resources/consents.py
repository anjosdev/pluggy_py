from requests import Response
from typing import Optional, List
from pluggy_py.utils.http_client import HttpClient
from pluggy_py.models.consents import PageResponseConsents, Consent

class ConsentsResource:
    """
    ConsentsResource handles the /consents endpoints:
      - List consents (GET /consents?itemId=<UUID>)
      - Retrieve a consent (GET /consents/{id})
    """

    def __init__(self, http_client: HttpClient, api_key: str):
        self._http = http_client
        self._api_key = api_key

    def list_consents(self, item_id: str, page: int = 1, page_size: int = 20) -> PageResponseConsents:
        """
        GET /consents?itemId=<UUID>&page=<page>&pageSize=<page_size>
        Retrieves a single page of consents for the given itemId.
        """
        headers = {"X-API-KEY": self._api_key}
        params = {"itemId": item_id, "page": page, "pageSize": page_size}
        response: Response = self._http.get("/consents", params=params, headers=headers)
        return PageResponseConsents(**response.json())

    def list_all_consents(self, item_id: str, page_size: int = 50) -> List[Consent]:
        """
        Fetches *all* consents by paging internally until the last page is reached.
        Returns a list of Consent objects.
        """
        headers = {"X-API-KEY": self._api_key}
        all_consents: List[Consent] = []
        page = 1

        while True:
            params = {"itemId": item_id, "page": page, "pageSize": page_size}
            response: Response = self._http.get("/consents", params=params, headers=headers)
            page_response = PageResponseConsents(**response.json())
            all_consents.extend(page_response.results)

            if page >= page_response.totalPages:
                break

            page += 1

        return all_consents

    def retrieve_consent(self, consent_id: str) -> Consent:
        """
        GET /consents/{id}
        Retrieves a single consent by its ID.
        """
        headers = {"X-API-KEY": self._api_key}
        response: Response = self._http.get(f"/consents/{consent_id}", headers=headers)
        return Consent(**response.json())

