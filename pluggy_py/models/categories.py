from typing import Optional, List
from pydantic import BaseModel, Field


class Category(BaseModel):
    """
    Represents a Category object returned by the /categories and /categories/{id} endpoints.
    """
    id: str = Field(..., description="Identifier for the category")
    description: str = Field(..., description="Description of the category")
    descriptionTranslated: Optional[str] = Field(
        None, description="Description of the category, translated to portuguese"
    )
    parentId: Optional[str] = Field(None, description="Parent's identifier")
    parentDescription: Optional[str] = Field(None, description="Parent's category description")


class PageResponseCategories(BaseModel):
    """
    Used for GET /categories responses, which return paging fields plus a list of Category objects.
    Example from the OAS snippet:
      {
        "page": 1,
        "total": 2,
        "totalPages": 1,
        "results": [ ...Category... ]
      }
    """
    page: int
    total: int
    totalPages: int
    results: List[Category]


class ClientCategoryRule(BaseModel):
    """
    Represents the created/returned category rule.
    According to the snippet, response from GET or POST /categories/rules.
    """
    description: str = Field(..., description="Description of the transaction rule.")
    categoryId: Optional[str] = Field(None, description="Identifier of the category")
    category: Optional[str] = Field(None, description="Description of the category")
    clientId: Optional[str] = Field(None, description="Identifier of the client")
    transactionType: Optional[str] = Field(None, description="Transaction type (DEBIT/CREDIT)")
    accountType: Optional[str] = Field(None, description="Account type (CHECKING_ACCOUNT/CREDIT_CARD)")


class PageResponseCategoryRules(BaseModel):
    """
    This wraps the list of client category rules in a paginated structure if needed.
    Some OAS references show that /categories/rules returns an array,
    or it might return a page object. We'll model it as:
      {
        "page": 1,
        "total": 2,
        "totalPages": 1,
        "results": [ ...ClientCategoryRule... ]
      }
    Adjust if your actual response differs.
    """
    page: int
    total: int
    totalPages: int
    results: List[ClientCategoryRule]


class CreateClientCategoryRule(BaseModel):
    """
    Model for the POST /categories/rules request body.
    """
    description: str = Field(..., description="Description of the transaction rule.")
    categoryId: str = Field(..., description="Identifier of the category")
    transactionType: Optional[str] = Field(None, description="Transaction type (DEBIT/CREDIT)")
    accountType: Optional[str] = Field(None, description="Account type (CHECKING_ACCOUNT/CREDIT_CARD)")
    matchType: Optional[str] = Field(
        None,
        description="Type of match used to identify the rule (exact|contains|startsWith|endsWith). Defaults to 'exact'"
    )
