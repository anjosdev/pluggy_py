from typing import Optional, List
from requests import Response
from pluggy_py.utils.http_client import HttpClient
from pluggy_py.models.bills import Bill, PageResponseBills

class BillsResource:
    """
    BillsResource handles the /bills endpoints:
      - List bills (GET /bills?accountId=...)
      - Retrieve a single bill (GET /bills/{id})
      - List ALL bills (list_all_bills).
    """

    def __init__(self, http_client: HttpClient, api_key: str):
        self._http_client = http_client
        self._api_key = api_key

    def list_bills(
        self,
        account_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> PageResponseBills:
        """
        GET /bills?accountId={account_id}&page={page}&pageSize={page_size}
        Returns a single page of credit card bills.
        """
        headers = {"X-API-KEY": self._api_key}
        params = {"accountId": account_id}

        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["pageSize"] = page_size

        response: Response = self._http_client.get("/bills", params=params, headers=headers)
        return PageResponseBills(**response.json())

    def retrieve_bill(self, bill_id: str) -> Bill:
        """
        GET /bills/{id}
        Retrieve a single bill by its primary identifier.
        """
        headers = {"X-API-KEY": self._api_key}
        response: Response = self._http_client.get(f"/bills/{bill_id}", headers=headers)
        return Bill(**response.json())

    def list_all_bills(
        self,
        account_id: str,
        page_size: int = 50,
    ) -> List[Bill]:
        """
        Returns ALL bills for the given account_id, by paging internally 
        until the last page is reached.
        """
        all_bills: List[Bill] = []
        page = 1

        while True:
            params = {"accountId": account_id, "page": page, "pageSize": page_size}
            headers = {"X-API-KEY": self._api_key}
            resp: Response = self._http_client.get("/bills", params=params, headers=headers)
            page_data = PageResponseBills(**resp.json())

            all_bills.extend(page_data.results)

            if page >= page_data.totalPages:
                break

            page += 1

        return all_bills
