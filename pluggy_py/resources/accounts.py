from typing import Optional, List
from pluggy_py.models.accounts import Account, PageResponseAccounts

class AccountsResource:
    def __init__(self, http_client, api_key: str):
        self._http = http_client
        self._api_key = api_key

    def list_accounts(
        self,
        item_id: str,
        account_type: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PageResponseAccounts:
        """
        Existing method that fetches a single page of accounts.
        """
        headers = {"X-API-KEY": self._api_key}
        params = {"itemId": item_id, "page": page, "pageSize": page_size}
        if account_type:
            params["type"] = account_type
        resp = self._http.get("/accounts", params=params, headers=headers)
        data = resp.json()
        return PageResponseAccounts(**data)

    def retrieve_account(self, account_id: str) -> Account:
        """
        Existing method to retrieve a single account by ID.
        """
        headers = {"X-API-KEY": self._api_key}
        resp = self._http.get(f"/accounts/{account_id}", headers=headers)
        data = resp.json()
        return Account(**data)

    def list_all_accounts(
        self,
        item_id: str,
        account_type: Optional[str] = None,
        page_size: int = 50
    ) -> List[Account]:
        """
        Method that returns ALL accounts from all pages, looping internally until
        totalPages is reached.
        """
        headers = {"X-API-KEY": self._api_key}
        all_accounts: List[Account] = []

        page = 1
        while True:
            # Fetch one page
            params = {"itemId": item_id, "page": page, "pageSize": page_size}
            if account_type:
                params["type"] = account_type

            resp = self._http.get("/accounts", params=params, headers=headers)
            data = resp.json()
            page_response = PageResponseAccounts(**data)

            # Add the results to our all_accounts list
            all_accounts.extend(page_response.results)

            # Check if we've reached the last page
            if page >= page_response.totalPages:
                break
            page += 1

        return all_accounts
