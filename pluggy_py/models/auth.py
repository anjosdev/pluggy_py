from datetime import datetime
from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    """
    AuthRequest model for the /auth endpoint.

    According to the OAS snippet, this request body requires:
    - clientId (str)
    - clientSecret (str)
    """

    clientId: str = Field(..., description="Client ID provided by Pluggy")
    clientSecret: str = Field(..., description="Client Secret provided by Pluggy")


class AuthResponse(BaseModel):
    """
    AuthResponse model for the /auth endpoint.

    This is the expected success response for the /auth POST call, which returns an API key.
    The Pluggy OAS includes (at minimum) 'accessToken', 'createdAt', and 'expiresIn'.
    Consult the official OAS for any additional fields.
    """

    apiKey: str = Field(..., description="Generated API Key")
    # createdAt: datetime = Field(..., description="Timestamp of token creation")
    # expiresIn: int = Field(
    #     ..., description="Number of seconds until the API Key expires"
    # )
