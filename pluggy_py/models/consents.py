from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Consent(BaseModel):
    id: str = Field(..., description="Consent primary identifier")
    itemId: str = Field(..., description="Associated Item identifier")
    products: Optional[List[str]] = Field(None, description="Products included in the consent")
    openFinancePermissionsGranted: Optional[List[str]] = Field(
        None, description="Open Finance permissions included in the consent"
    )
    createdAt: Optional[datetime] = Field(None, description="Timestamp of consent creation")
    expiresAt: Optional[datetime] = Field(None, description="Timestamp of when consent expires")
    revokedAt: Optional[datetime] = Field(None, description="Timestamp of when consent was revoked, if any")


class PageResponseConsents(BaseModel):
    total: int
    totalPages: int
    page: int
    results: List[Consent] = Field(
        ..., description="List of retrieved consent objects"
    )

