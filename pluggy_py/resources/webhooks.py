from typing import Optional, List
from pluggy_py.utils.http_client import HttpClient
from pluggy_py.models.webhooks import (
    Webhook,
    CreateWebhookRequest,
    PageResponseWebhooks,
)
from pluggy_py.models.items import ICountResponse  # Reuse for DELETE response

class WebhooksResource:
    def __init__(self, http_client: HttpClient, api_key: str):
        self._http = http_client
        self._api_key = api_key

    def list_webhooks(self, page: int = 1, page_size: int = 20) -> PageResponseWebhooks:
        """
        GET /webhooks - Retrieves all Webhooks in a paginated response.
        """
        headers = {"X-API-KEY": self._api_key}
        params = {"page": page, "pageSize": page_size}
        response = self._http.get("/webhooks", params=params, headers=headers)
        return PageResponseWebhooks(**response.json())

    def list_all_webhooks(self, page_size: int = 50) -> List[Webhook]:
        """
        Returns ALL webhooks, paging internally until the last page is reached.
        """
        all_hooks: List[Webhook] = []
        page = 1

        while True:
            page_response = self.list_webhooks(page=page, page_size=page_size)
            all_hooks.extend(page_response.results)

            if page >= page_response.totalPages:
                break
            page += 1

        return all_hooks

    def create_webhook(self, data: CreateWebhookRequest) -> Webhook:
        """
        POST /webhooks - Creates a new Webhook.
        """
        headers = {"X-API-KEY": self._api_key}
        response = self._http.post("/webhooks", json=data.dict(exclude_none=True), headers=headers)
        return Webhook(**response.json())

    def retrieve_webhook(self, webhook_id: str) -> Webhook:
        """
        GET /webhooks/{id} - Retrieves a specific Webhook.
        """
        headers = {"X-API-KEY": self._api_key}
        url = f"/webhooks/{webhook_id}"
        response = self._http.get(url, headers=headers)
        return Webhook(**response.json())

    def update_webhook(self, webhook_id: str, data: CreateWebhookRequest) -> Webhook:
        """
        PATCH /webhooks/{id} - Updates a webhook (e.g., event, url, or headers).
        """
        headers = {"X-API-KEY": self._api_key}
        url = f"/webhooks/{webhook_id}"
        response = self._http.patch(url, json=data.dict(exclude_none=True), headers=headers)
        return Webhook(**response.json())

    def delete_webhook(self, webhook_id: str) -> ICountResponse:
        """
        DELETE /webhooks/{id} - Deletes the specified webhook.
        Returns a body with the 'count' field, e.g. {'count': 1}
        """
        headers = {"X-API-KEY": self._api_key}
        url = f"/webhooks/{webhook_id}"
        response = self._http.delete(url, headers=headers)
        return ICountResponse(**response.json())
