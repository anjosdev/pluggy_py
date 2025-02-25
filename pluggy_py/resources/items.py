import os
import sys
from typing import Dict, Any
from requests import Response

from pluggy_py.utils.http_client import HttpClient
from pluggy_py.models.items import (
    CreateItemRequest,
    UpdateItemRequest,
    Item,
    ICountResponse,
)

class ItemsResource:
    """
    ItemsResource handles the /items endpoints:
      - Create an item (POST /items)
      - Retrieve an item (GET /items/{id})
      - Update an item (PATCH /items/{id})
      - Delete an item (DELETE /items/{id})
      - Send MFA (POST /items/{id}/mfa)
    """

    def __init__(self, http_client: HttpClient, api_key: str):
        """
        :param http_client: An HttpClient instance for making requests
        :param api_key: The API key obtained via authentication
        """
        self.http_client = http_client
        self.api_key = api_key

    def create_item(self, create_data: CreateItemRequest) -> Item:
        """
        POST /items
        Creates an item based on the provided credentials and connector.
        """
        headers = {"X-API-KEY": self.api_key}
        response: Response = self.http_client.post(
            "/items",
            json=create_data.dict(exclude_none=True),
            headers=headers,
        )
        # Let the _http client handle exceptions if the response is not 2xx.
        return Item(**response.json())

    def retrieve_item(self, item_id: str) -> Item:
        """
        GET /items/{id}
        Retrieves the item resource by its ID.
        """
        headers = {"X-API-KEY": self.api_key}
        response: Response = self.http_client.get(
            f"/items/{item_id}",
            headers=headers,
        )
        return Item(**response.json())

    def retrieve_yaml_items(self, yaml_path: str = None) -> list[dict[str, str]]:
        """
        Reads a YAML file mapping item names to IDs and returns them 
        as a list of dicts with the format [{'name': <yaml_key>, 'id': <yaml_value>}].
        
        :param yaml_path: Optional path to the items.yaml file. Defaults to package's items.yaml.
        :return: A list of dict objects.
        """
        if not yaml_path:
            script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            yaml_path = os.path.join(script_dir, "items.yaml")

        with open(yaml_path, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines()

        results = []
        for line in lines:
            if ":" not in line:
                continue
            key, value = line.split(":", maxsplit=1)
            key = key.strip()
            value = value.strip()
            results.append({"name": key, "id": value})

        return results

    def update_item(self, item_id: str, update_data: UpdateItemRequest) -> Item:
        """
        PATCH /items/{id}
        Updates an existing item with new credentials, triggers new sync, etc.
        """
        headers = {"X-API-KEY": self.api_key}
        response: Response = self.http_client.patch(
            f"/items/{item_id}",
            json=update_data.dict(exclude_none=True),
            headers=headers,
        )
        return Item(**response.json())

    def delete_item(self, item_id: str) -> ICountResponse:
        """
        DELETE /items/{id}
        Deletes an item by its primary identifier.
        Returns a simple count-based response or an error if not found.
        """
        headers = {"X-API-KEY": self.api_key}
        response: Response = self.http_client.delete(
            f"/items/{item_id}",
            headers=headers,
        )
        return ICountResponse(**response.json())

    def send_mfa(self, item_id: str, mfa_values: Dict[str, Any]) -> Item:
        """
        POST /items/{id}/mfa
        When an item is in MFA (multi-factor) state, sends user-provided MFA data.
        """
        headers = {"X-API-KEY": self.api_key}
        response: Response = self.http_client.post(
            f"/items/{item_id}/mfa",
            json=mfa_values,
            headers=headers,
        )
        return Item(**response.json())
