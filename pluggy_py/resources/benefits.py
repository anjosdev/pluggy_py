from typing import List
from pluggy_py.models.benefits import Benefit, PageResponseBenefits
from pluggy_py.utils.http_client import HttpClient
from pluggy_py.exceptions import PluggyAPIError

class BenefitsResource:
    """
    BenefitsResource handles the /benefits endpoints:
      - GET /benefits?itemId=...
      - GET /benefits/{id}
    """

    def __init__(self, http_client: HttpClient, api_key: str):
        self._http = http_client
        self._api_key = api_key

    def list_benefits(
        self, 
        item_id: str, 
        page: int = 1, 
        page_size: int = 20
    ) -> PageResponseBenefits:
        """
        GET /benefits?itemId={itemId}&page={page}&pageSize={pageSize}
        Lists benefits for a given itemId.
        """
        headers = {"X-API-KEY": self._api_key}
        params = {"itemId": item_id, "page": page, "pageSize": page_size}

        response = self._http.get("/benefits", params=params, headers=headers)
        return PageResponseBenefits(**response.json())

    def list_all_benefits(
        self, 
        item_id: str, 
        page_size: int = 50
    ) -> List[Benefit]:
        """
        Fetches *all* benefits by paging internally until the last page is reached.
        Returns a list of Benefit objects.
        """
        headers = {"X-API-KEY": self._api_key}
        all_benefits: List[Benefit] = []
        page = 1

        while True:
            params = {"itemId": item_id, "page": page, "pageSize": page_size}
            response = self._http.get("/benefits", params=params, headers=headers)
            page_response = PageResponseBenefits(**response.json())
            all_benefits.extend(page_response.results)

            if page >= page_response.totalPages:
                break

            page += 1

        return all_benefits

    def retrieve_benefit(self, benefit_id: str) -> Benefit:
        """
        GET /benefits/{id}
        Retrieve a single benefit by its primary identifier.
        """
        headers = {"X-API-KEY": self._api_key}
        response = self._http.get(f"/benefits/{benefit_id}", headers=headers)
        return Benefit(**response.json())
