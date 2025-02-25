from requests import Response
from typing import Optional, List
from pluggy_py.utils.http_client import HttpClient
from pluggy_py.models.categories import (
    Category,
    PageResponseCategories,
    ClientCategoryRule,
    PageResponseCategoryRules,
    CreateClientCategoryRule,
)

class CategoriesResource:
    """
    CategoriesResource handles:
      - GET /categories
      - GET /categories/{id}
      - GET /categories/rules
      - POST /categories/rules
    """

    def __init__(self, http_client: HttpClient, api_key: str):
        self._http = http_client
        self._api_key = api_key

    def list_categories(
        self, 
        parent_id: Optional[str] = None, 
        page: int = 1, 
        page_size: int = 20
    ) -> PageResponseCategories:
        """
        GET /categories
        Can be filtered by 'parentId' if provided.
        Returns a paginated structure with all categories.
        """
        headers = {"X-API-KEY": self._api_key}
        params = {"page": page, "pageSize": page_size}
        if parent_id:
            params["parentId"] = parent_id

        response: Response = self._http.get("/categories", params=params, headers=headers)
        return PageResponseCategories(**response.json())

    def list_all_categories(
        self, 
        parent_id: Optional[str] = None, 
        page_size: int = 50
    ) -> List[Category]:
        """
        Fetches *all* categories by paging internally until the last page is reached.
        Returns a list of Category objects.
        """
        headers = {"X-API-KEY": self._api_key}
        all_categories: List[Category] = []
        page = 1

        while True:
            params = {"page": page, "pageSize": page_size}
            if parent_id:
                params["parentId"] = parent_id

            response: Response = self._http.get("/categories", params=params, headers=headers)
            page_response = PageResponseCategories(**response.json())
            all_categories.extend(page_response.results)

            if page >= page_response.totalPages:
                break

            page += 1

        return all_categories

    def retrieve_category(self, category_id: str) -> Category:
        """
        GET /categories/{id}
        Retrieves a single category by its id.
        """
        headers = {"X-API-KEY": self._api_key}
        response: Response = self._http.get(f"/categories/{category_id}", headers=headers)
        return Category(**response.json())

    def list_category_rules(self) -> PageResponseCategoryRules:
        """
        GET /categories/rules
        Retrieves client category rules in a paginated structure.
        """
        headers = {"X-API-KEY": self._api_key}
        response: Response = self._http.get("/categories/rules", headers=headers)
        return PageResponseCategoryRules(**response.json())

    def create_category_rule(self, rule_data: CreateClientCategoryRule) -> ClientCategoryRule:
        """
        POST /categories/rules
        Creates a single category rule and returns the created rule.
        """
        headers = {"X-API-KEY": self._api_key}
        response: Response = self._http.post(
            "/categories/rules",
            json=rule_data.dict(exclude_none=True),
            headers=headers
        )
        return ClientCategoryRule(**response.json())
