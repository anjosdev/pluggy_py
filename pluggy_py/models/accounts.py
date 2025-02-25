from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class BankData(BaseModel):
    transferNumber: Optional[str] = None
    closingBalance: Optional[float] = None
    automaticallyInvestedBalance: Optional[float] = None

class CreditData(BaseModel):
    level: Optional[str] = None
    brand: Optional[str] = None
    balanceCloseDate: Optional[str] = None
    balanceDueDate: Optional[str] = None
    availableCreditLimit: Optional[float] = None
    balanceForeignCurrency: Optional[float] = None
    minimumPayment: Optional[float] = None
    creditLimit: Optional[float] = None
    status: Optional[str] = None
    holderType: Optional[str] = None

class Account(BaseModel):
    """
    Represents the 'Account' resource from Pluggy API.
    """
    id: str
    type: str
    subtype: Optional[str] = None
    number: Optional[str] = None
    name: Optional[str] = None
    marketingName: Optional[str] = None
    balance: Optional[float] = None
    itemId: Optional[str] = None
    taxNumber: Optional[str] = None
    owner: Optional[str] = None
    currencyCode: Optional[str] = None
    bankData: Optional[BankData] = None
    creditData: Optional[CreditData] = None

class PageResponseAccounts(BaseModel):
    """
    Used for GET /accounts response:
      {
        "page": 1,
        "total": 2,
        "totalPages": 1,
        "results": [ ...accounts... ]
      }
    """
    page: int
    total: int
    totalPages: int
    results: List[Account] = Field(..., description="List of retrieved accounts")

