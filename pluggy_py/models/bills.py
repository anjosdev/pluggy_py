from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class BillFinanceCharge(BaseModel):
    id: Optional[str] = Field(None, description="Finance charge identifier")
    type: Optional[str] = Field(None, description="Type of the finance charge (IOF, LATE_PAYMENT_INTEREST, etc.)")
    amount: Optional[float] = Field(None, description="Amount of this charge/fee")
    currencyCode: Optional[str] = Field(None, description="Currency code, e.g. BRL")
    additionalInfo: Optional[str] = Field(None, description="Free text for additional information if needed")

class Bill(BaseModel):
    """
    Represents a credit card bill resource from the Pluggy API.
    """
    id: str = Field(..., description="Primary identifier of the Bill")
    accountId: Optional[str] = Field(None, description="Account ID to which this bill belongs")
    dueDate: Optional[datetime] = Field(None, description="Due date of the bill")
    totalAmount: Optional[float] = Field(None, description="Total amount of the bill")
    totalAmountCurrencyCode: Optional[str] = Field(None, description="Currency code of the totalAmount, e.g. BRL")
    minimumPaymentAmount: Optional[float] = Field(None, description="Minimum payment required")
    allowsInstallments: Optional[bool] = Field(None, description="Whether the bill allows installments")
    financeCharges: Optional[List[BillFinanceCharge]] = Field(
        None, description="List of charges associated with this bill"
    )

class PageResponseBills(BaseModel):
    """
    Used for GET /bills response, which returns paging plus a list of Bill objects.
    Example response structure:
      {
        "page": 1,
        "total": 1,
        "totalPages": 1,
        "results": [ ...Bill objects... ]
      }
    """
    page: int
    total: int
    totalPages: int
    results: List[Bill] = Field(..., description="List of credit card bills")
