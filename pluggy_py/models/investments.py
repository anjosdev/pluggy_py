from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class InvestmentTransaction(BaseModel):
    id: Optional[str] = Field(None, description="Transaction primary identifier")
    amount: Optional[float] = Field(None, description="Gross amount of the transaction")
    description: Optional[str] = Field(None, description="Raw description of the transaction")
    value: Optional[float] = Field(None, description="Quota's current value at the transaction date")
    quantity: Optional[float] = Field(None, description="Quantity of quota bought or sold")
    tradeDate: Optional[datetime] = Field(None, description="Date when the trade was made")
    date: Optional[datetime] = Field(None, description="Date considered for the transaction settlement")
    type: Optional[str] = Field(None, description="BUY, SELL, etc.")
    movementType: Optional[str] = Field(None, description="CREDIT, DEBIT, etc.")
    netAmount: Optional[float] = Field(None, description="Net amount after fees, if any")
    agreedRate: Optional[float] = Field(None, description="Rate if applicable (CDI, etc.)")
    brokerageNumber: Optional[str] = Field(None, description="Reference number if provided")
    expenses: Optional[dict] = Field(None, description="Any extra fees, described as an object or dict")

class Investment(BaseModel):
    id: str = Field(..., description="Primary identifier of the investment")
    itemId: str = Field(..., description="Identifier of the item linked to the investment")
    type: str = Field(..., description="Investment asset type (MUTUAL_FUND, FIXED_INCOME, SECURITY, etc.)")
    subtype: Optional[str] = Field(None, description="Investment subtype (e.g. CDB, MULTIMARKET_FUND, etc.)")
    number: Optional[str] = None
    name: Optional[str] = None
    balance: float = Field(..., description="Net balance amount of the investment")
    currencyCode: Optional[str] = None
    code: Optional[str] = Field(None, description="Associated code for the investment (e.g. fund CNPJ)")
    isin: Optional[str] = Field(None, description="12-character ISIN, globally unique")
    lastMonthRate: Optional[float] = None
    lastTwelveMonthsRate: Optional[float] = None
    annualRate: Optional[float] = None
    value: Optional[float] = Field(None, description="Quota's current value at 'date'")
    quantity: Optional[float] = Field(None, description="Quantity of quota at disposal")
    amount: Optional[float] = Field(None, description="Gross amount of the investment")
    taxes: Optional[float] = None
    taxes2: Optional[float] = None
    date: datetime = Field(..., description="Quota date or last updated date for the investment")
    owner: Optional[str] = None
    amountProfit: Optional[float] = None
    amountWithdrawal: Optional[float] = None
    amountOriginal: Optional[float] = None
    status: Optional[str] = Field(None, description="ACTIVE, PENDING, etc.")
    issuer: Optional[str] = Field(None, description="The entity that issued the investment, if relevant")
    issuerCNPJ: Optional[str] = None
    issueDate: Optional[datetime] = None
    rate: Optional[float] = None
    rateType: Optional[str] = None
    fixedAnnualRate: Optional[float] = None
    # You can add more fields (dueDate, metadata, etc.) according to your needs
    # transactions: Optional[List[InvestmentTransaction]] = None  # Sometimes the single GET includes transactions

class PageResponseInvestments(BaseModel):
    page: int
    total: int
    totalPages: int
    results: List[Investment] = Field(..., description="List of investments")

class PageResponseInvestmentTransactions(BaseModel):
    page: int
    total: int
    totalPages: int
    results: List[InvestmentTransaction] = Field(..., description="List of transactions for a specific investment")
