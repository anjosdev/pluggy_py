from pluggy_py.models.auth import AuthRequest, AuthResponse
from pluggy_py.utils.http_client import HttpClient
from requests import Response


class AuthResource:
    """
    AuthResource handles all calls to Pluggy's /auth endpoint.
    It encapsulates logic for creating an API key.
    """

    def __init__(self, http_client: HttpClient):
        """
        Initialize the AuthResource.

        :param http_client: A shared or dedicated HTTP client for making requests.
        """
        self._http_client = http_client

    def create_api_key(self, auth_request: AuthRequest) -> AuthResponse:
        """
        Create an API key using the provided clientId and clientSecret.

        :param auth_request: AuthRequest object containing clientId and clientSecret.
        :return: AuthResponse with generated apiKey.
        :raises PluggyAPIError: If the request fails or returns an error.
        """
        response: Response = self._http_client.post(
            "/auth", json=auth_request.dict(exclude_none=True)
        )
        return AuthResponse(**response.json())
