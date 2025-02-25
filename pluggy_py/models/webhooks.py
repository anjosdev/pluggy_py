from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field

class Webhook(BaseModel):
    """
    Represents a Webhook resource from Pluggy.
    Schema based on oas3.json (webhooks snippet).
    """
    id: str = Field(..., description="UUID identifier for the webhook")
    url: str = Field(..., description="Listener URL for the webhook notification")
    event: str = Field(..., description="Event name, e.g. 'item/created', 'item/updated', etc.")
    disabledAt: Optional[datetime] = Field(None, description="Timestamp when the webhook was disabled")
    createdAt: Optional[datetime] = Field(None, description="Timestamp when the webhook was created")
    updatedAt: Optional[datetime] = Field(None, description="Timestamp when the webhook was last updated")

class CreateWebhookRequest(BaseModel):
    """
    Create/Update request body for webhook (oas3.json #/components/requestBodies/CreateWebhook).
    """
    url: str = Field(..., description="Endpoint to receive the notifications")
    event: str = Field(..., description="Event name, e.g. 'item/updated', 'item/all', etc.")
    headers: Optional[Dict[str, str]] = Field(None, description="Optional HTTP headers attached to the webhook call")

class PageResponseWebhooks(BaseModel):
    """
    Paging structure for GET /webhooks
    {
      "page": 1,
      "total": 2,
      "totalPages": 1,
      "results": [Webhook, Webhook, ...]
    }
    """
    page: int
    total: int
    totalPages: int
    results: List[Webhook] = Field(..., description="List of Webhooks")
