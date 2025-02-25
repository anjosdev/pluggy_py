import requests
from urllib.parse import urljoin
from pluggy_py.exceptions import (
    GlobalErrorResponse,
    BadRequestError,
    UnauthorizedError,
    NotFoundError,
    ConflictError,
    InternalServerError,
    PluggyAPIError,
)

class HttpClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _get_full_url(self, path: str) -> str:
        return urljoin(self.base_url + "/", path.lstrip("/"))

    def _handle_response(self, response: requests.Response) -> requests.Response:
        """Check for non-2xx responses, parse error details, and raise if needed."""
        if response.ok:
            return response  # 2xx => success

        # Try to parse JSON error details
        try:
            error_data = response.json()
            # Typically: { "code": 404, "codeDescription": "ITEM_NOT_FOUND", "message": "item not found" }
            code = error_data.get("code", response.status_code)
            code_description = error_data.get("codeDescription", "")
            message = error_data.get("message", response.reason)
        except Exception:
            # Fallback if JSON parse fails
            code = response.status_code
            code_description = ""
            message = response.text or response.reason

        # Now map status_code to a specialized exception
        if response.status_code == 400:
            raise BadRequestError(code, code_description, message)
        elif response.status_code == 401:
            raise UnauthorizedError(code, code_description, message)
        elif response.status_code == 404:
            raise NotFoundError(code, code_description, message)
        elif response.status_code == 409:
            raise ConflictError(code, code_description, message)
        elif response.status_code >= 500:
            raise InternalServerError(code, code_description, message)
        else:
            # If we want to handle other codes or if it’s an unrecognized code, just raise a generic error
            raise GlobalErrorResponse(code, code_description, message)

    def get(self, path: str, params: dict = None, headers: dict = None) -> requests.Response:
        url = self._get_full_url(path)
        resp = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        return self._handle_response(resp)

    def post(self, path: str, json: dict = None, headers: dict = None) -> requests.Response:
        url = self._get_full_url(path)
        resp = self.session.post(url, json=json, headers=headers, timeout=self.timeout)
        return self._handle_response(resp)

    def put(self, path: str, json: dict = None, headers: dict = None) -> requests.Response:
        url = self._get_full_url(path)
        resp = self.session.put(url, json=json, headers=headers, timeout=self.timeout)
        return self._handle_response(resp)

    def delete(self, path: str, headers: dict = None) -> requests.Response:
        url = self._get_full_url(path)
        resp = self.session.delete(url, headers=headers, timeout=self.timeout)
        return self._handle_response(resp)

    def patch(self, path: str, json: dict = None, headers: dict = None) -> requests.Response:
        url = self._get_full_url(path)
        resp = self.session.patch(url, json=json, headers=headers, timeout=self.timeout)
        return self._handle_response(resp)
