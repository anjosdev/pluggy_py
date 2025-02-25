from typing import Optional, List
from requests import Response
from pluggy_py.utils.http_client import HttpClient
from pluggy_py.models.loans import Loan, PageResponseLoans

class LoansResource:
    """
    LoansResource handles the /loans endpoints:
      - List loans (GET /loans?itemId=...)
      - Retrieve a single loan (GET /loans/{id})
      - List ALL loans across multiple pages (list_all_loans).
    """

    def __init__(self, http_client: HttpClient, api_key: str):
        self._http_client = http_client
        self._api_key = api_key

    def list_loans(
        self,
        item_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> PageResponseLoans:
        """
        GET /loans?itemId={item_id}&page={page}&pageSize={page_size}
        Returns a single page of loans for the given itemId.
        """
        headers = {"X-API-KEY": self._api_key}
        params = {"itemId": item_id}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["pageSize"] = page_size

        # No need for a try/except here; _http_client.get() will raise on non-2xx
        resp: Response = self._http_client.get("/loans", params=params, headers=headers)
        return PageResponseLoans(**resp.json())

    def retrieve_loan(self, loan_id: str) -> Loan:
        """
        GET /loans/{id}
        Retrieve a single loan by its primary identifier.
        """
        headers = {"X-API-KEY": self._api_key}
        resp: Response = self._http_client.get(f"/loans/{loan_id}", headers=headers)
        return Loan(**resp.json())

    def list_all_loans(
        self,
        item_id: str,
        page_size: int = 50
    ) -> List[Loan]:
        """
        Returns ALL loans for the given item_id, by paging internally until the last page.
        """
        headers = {"X-API-KEY": self._api_key}
        all_loans: List[Loan] = []
        page = 1

        while True:
            params = {"itemId": item_id, "page": page, "pageSize": page_size}
            resp: Response = self._http_client.get("/loans", params=params, headers=headers)
            page_data = PageResponseLoans(**resp.json())

            all_loans.extend(page_data.results)

            if page >= page_data.totalPages:
                break

            page += 1

        return all_loans

