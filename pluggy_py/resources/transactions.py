from typing import Optional, List
from requests import Response
from pluggy_py.utils.http_client import HttpClient
from pluggy_py.exceptions import PluggyAPIError
from pluggy_py.models.transactions import Transaction, PageResponseTransactions, UpdateTransaction

class TransactionsResource:
    """
    TransactionsResource handles the /transactions endpoints:
      - GET /transactions
      - GET /transactions/{id}
      - PATCH /transactions/{id}
      - NEW: list_all_transactions to fetch all pages at once.
    """

    def __init__(self, http_client: HttpClient, api_key: str):
        self._http_client = http_client
        self._api_key = api_key

    def list_transactions(
        self,
        account_id: str,
        ids: Optional[List[str]] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
        bill_id: Optional[str] = None,
        created_at_from: Optional[str] = None,
    ) -> PageResponseTransactions:
        """
        Returns a single page of transactions. 
        GET /transactions?accountId=xxx
        """
        headers = {"X-API-KEY": self._api_key}
        params = {"accountId": account_id}

        if ids:
            params["ids"] = ",".join(ids)
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if page_size:
            params["pageSize"] = page_size
        if page:
            params["page"] = page
        if bill_id:
            params["billId"] = bill_id
        if created_at_from:
            params["createdAtFrom"] = created_at_from

        response: Response = self._http_client.get("/transactions", params=params, headers=headers)
        return PageResponseTransactions(**response.json())

    def list_all_transactions(
        self,
        account_id: str,
        ids: Optional[List[str]] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        bill_id: Optional[str] = None,
        created_at_from: Optional[str] = None,
        page_size: int = 50,
    ) -> List[Transaction]:
        """
        Fetches *all* transactions by paging internally until the last page is reached.
        Returns a list of Transaction objects.
        """
        all_transactions: List[Transaction] = []
        page = 1

        while True:
            page_response = self.list_transactions(
                account_id=account_id,
                ids=ids,
                from_date=from_date,
                to_date=to_date,
                bill_id=bill_id,
                created_at_from=created_at_from,
                page_size=page_size,
                page=page,
            )

            all_transactions.extend(page_response.results)

            if page >= page_response.totalPages:
                break

            page += 1

        return all_transactions

    def retrieve_transaction(self, transaction_id: str) -> Transaction:
        """
        GET /transactions/{id} - Retrieves a single transaction by its ID.
        """
        headers = {"X-API-KEY": self._api_key}
        response: Response = self._http_client.get(
            f"/transactions/{transaction_id}", headers=headers
        )
        return Transaction(**response.json())

    def update_transaction_category(self, transaction_id: str, category_id: str) -> Transaction:
        """
        PATCH /transactions/{id} - Updates the transaction's category by its ID.
        """
        headers = {"X-API-KEY": self._api_key}
        update_model = UpdateTransaction(categoryId=category_id)

        response: Response = self._http_client.patch(
            f"/transactions/{transaction_id}",
            json=update_model.dict(),
            headers=headers,
        )
        return Transaction(**response.json())
