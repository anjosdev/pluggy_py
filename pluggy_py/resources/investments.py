from typing import Optional, List
from requests import Response

from pluggy_py.utils.http_client import HttpClient
from pluggy_py.models.investments import (
    Investment,
    PageResponseInvestments,
    PageResponseInvestmentTransactions
)


class InvestmentsResource:
    """
    InvestmentsResource handles the /investments endpoints:
      - List all investments (GET /investments?itemId=xxx)
      - Retrieve a single investment by ID (GET /investments/{id})
      - List all transactions for a given investment (GET /investments/{id}/transactions)
      - NEW: list_all_investments to fetch all pages internally.
    """

    def __init__(self, http_client: HttpClient, api_key: str):
        self._http_client = http_client
        self._api_key = api_key

    def list_investments(
        self,
        item_id: str,
        type: Optional[str] = None,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
    ) -> PageResponseInvestments:
        """
        GET /investments?itemId={item_id}&type={type}&pageSize={page_size}&page={page}
        Returns a single page of investments for the given query parameters.
        """
        headers = {"X-API-KEY": self._api_key}
        params = {"itemId": item_id}

        if type:
            params["type"] = type
        if page_size is not None:
            params["pageSize"] = page_size
        if page is not None:
            params["page"] = page

        # _http.get now raises if non-2xx, so we do not need try/except or raise_for_status().
        response: Response = self._http_client.get("/investments", params=params, headers=headers)
        return PageResponseInvestments(**response.json())

    def retrieve_investment(self, investment_id: str) -> Investment:
        """
        GET /investments/{id}
        Retrieves a single Investment by its ID.
        """
        headers = {"X-API-KEY": self._api_key}
        response: Response = self._http_client.get(f"/investments/{investment_id}", headers=headers)
        return Investment(**response.json())

    def list_investment_transactions(
        self,
        investment_id: str,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
    ) -> PageResponseInvestmentTransactions:
        """
        GET /investments/{id}/transactions
        Returns a single page of transactions for the given investment.
        """
        headers = {"X-API-KEY": self._api_key}
        params = {}
        if page_size is not None:
            params["pageSize"] = page_size
        if page is not None:
            params["page"] = page

        response: Response = self._http_client.get(
            f"/investments/{investment_id}/transactions",
            params=params,
            headers=headers
        )
        return PageResponseInvestmentTransactions(**response.json())

    def list_all_investments(
        self,
        item_id: str,
        type: Optional[str] = None,
        page_size: int = 50
    ) -> List[Investment]:
        """
        NEW METHOD:
        Fetches all investments for the given itemId (and optional type) by paging
        internally until the last page is reached. Returns a list of Investment objects.
        """
        all_investments: List[Investment] = []
        page = 1

        while True:
            page_response = self.list_investments(
                item_id=item_id,
                type=type,
                page_size=page_size,
                page=page,
            )
            all_investments.extend(page_response.results)

            if page >= page_response.totalPages:
                break
            page += 1

        return all_investments

