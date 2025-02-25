from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class DocumentNumber(BaseModel):
    """
    Represents a sub-object for document identification, such as CPF or CNPJ.
    """
    type: Optional[str] = Field(None, description="Document type (CPF, CNPJ, etc.)")
    value: Optional[str] = Field(None, description="Document value (e.g. '882.937.076-23')")


class PaymentParty(BaseModel):
    """
    Represents common data for 'payer' or 'receiver' in PaymentData.
    """
    name: Optional[str] = None
    branchNumber: Optional[str] = None
    accountNumber: Optional[str] = None
    routingNumber: Optional[str] = None
    documentNumber: Optional[DocumentNumber] = None


class PaymentData(BaseModel):
    """
    Data regarding payments, as referenced by Transaction.paymentData.
    """
    payer: Optional[PaymentParty] = Field(None, description="Payer information")
    reason: Optional[str] = Field(None, description="Reason for the payment")
    receiver: Optional[PaymentParty] = Field(None, description="Receiver information")
    paymentMethod: Optional[str] = Field(None, description="Payment method (e.g. 'PIX', 'TED')")
    referenceNumber: Optional[str] = Field(None, description="Payment reference number")


class CreditCardMetadata(BaseModel):
    """
    Data of a transaction specific to credit card transactions.
    """
    installmentNumber: Optional[int] = Field(None, description="Number of the current installment of the purchase")
    totalInstallments: Optional[int] = Field(None, description="Total number of installments of the purchase")
    totalAmount: Optional[float] = Field(None, description="Total amount of the purchase")
    purchaseDate: Optional[datetime] = Field(None, description="Original Date of the purchase")
    payeeMCC: Optional[int] = Field(None, description="Merchant Category Code of the merchant")
    cardNumber: Optional[str] = Field(None, description="Credit Card Number used, can be different from account if it's an additional or virtual card")
    billId: Optional[str] = Field(None, description="Id of the bill associated to this transaction")


class Merchant(BaseModel):
    """
    Data about the merchant or payee for the transaction.
    """
    name: Optional[str] = Field(None, description="Display name of the merchant")
    businessName: Optional[str] = Field(None, description="Legal or business name")
    cnpj: Optional[str] = Field(None, description="CNPJ number if in Brazil")
    category: Optional[str] = Field(None, description="Merchant category")
    cnae: Optional[str] = Field(None, description="Merchant CNAE code")


class Transaction(BaseModel):
    """
    Represents a 'Transaction' resource from the Pluggy API,
    following the OAS snippet with additional fields.
    """
    id: str = Field(..., description="Primary identifier of the transaction")
    description: Optional[str] = Field(None, description="Clean description of the transaction")
    descriptionRaw: Optional[str] = Field(None, description="Raw description if provided")
    currencyCode: Optional[str] = Field(None, description="Currency ISO code")
    amount: float = Field(..., description="Transaction amount")
    amountInAccountCurrency: Optional[float] = Field(
        None, 
        description="Transaction amount in the account's currency if different from the original currency"
    )
    date: datetime = Field(..., description="Date when the transaction was made")
    type: Optional[str] = Field(None, description="DEBIT (outflow) or CREDIT (inflow)")
    balance: Optional[float] = Field(None, description="Balance after the transaction")
    providerCode: Optional[str] = Field(None, description="Institution-provided code")
    status: Optional[str] = Field(None, description="Status of the transaction (POSTED, PENDING, etc.)")
    category: Optional[str] = Field(None, description="Human-friendly category of the transaction (e.g. Restaurants)")
    categoryId: Optional[str] = Field(None, description="ID of the transaction category to match the Categories endpoint")
    operationType: Optional[str] = Field(None, description="Type of operation classified by the institution")
    paymentData: Optional[PaymentData] = Field(None, description="Payment data for the transaction if relevant")
    creditCardMetadata: Optional[CreditCardMetadata] = Field(None, description="Credit card-specific data for this transaction")
    merchant: Optional[Merchant] = Field(None, description="Information about the merchant for this transaction")
    accountId: Optional[str] = Field(None, description="The accountId to which this transaction belongs")


class PageResponseTransactions(BaseModel):
    """
    Used for GET /transactions responses:
      {
        "total": 8,
        "totalPages": 1,
        "page": 1,
        "results": [ ...Transaction... ]
      }
    """
    total: int
    totalPages: int
    page: int
    results: List[Transaction] = Field(..., description="List of retrieved transactions")


class UpdateTransaction(BaseModel):
    """
    Model for PATCH /transactions/{id} to update the transaction category.
    """
    category: str = Field(..., description="The new category identifier")
