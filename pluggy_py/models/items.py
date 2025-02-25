from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class CreateItemRequest(BaseModel):
    """Model for creating an Item via POST /items."""
    connectorId: int = Field(..., description="Connector primary identifier")
    parameters: Dict[str, Any] = Field(..., description="Credentials or parameters for the connector")
    webhookUrl: Optional[str] = Field(None, description="Optional webhook to notify about item updates")
    clientUserId: Optional[str] = Field(None, description="Optional ID to correlate the user on your side")


class UpdateItemRequest(BaseModel):
    """Model for updating an Item via PATCH /items/{id}."""
    parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters or credentials to update")
    webhookUrl: Optional[str] = Field(None, description="New or updated webhook")
    clientUserId: Optional[str] = Field(None, description="New or updated user reference")


class Item(BaseModel):
    """Represents the Item resource returned by Pluggy."""
    id: str
    name: Optional[str] = None
    connectorId: Optional[int] = None
    status: Optional[str] = None
    executionStatus: Optional[str] = None
    parameterNames: Optional[Dict[str, Any]] = None
    # Add other fields if desired, according to your OAS definition

    # Example minimal usage:
    # "id": "d0f8a8c0-e8e3-11e9-b210-d663bd873d93"
    # "status": "UPDATED"
    # "executionStatus": "SUCCESS"


class ICountResponse(BaseModel):
    """Represents the response body for a deletion (or any count-based response) from /items."""
    count: int

