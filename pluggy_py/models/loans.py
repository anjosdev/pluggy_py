from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class LoanPaymentReleaseOverParcelCharge(BaseModel):
    type: Optional[str] = Field(None, description="Charge type agreed in the contract")
    additionalInfo: Optional[str] = Field(None, description="Free field for additional info about the charge")
    amount: Optional[float] = Field(None, description="Payment amount of the charge paid outside the installment")

class LoanPaymentReleaseOverParcelFee(BaseModel):
    name: Optional[str] = Field(None, description="Denomination of the agreed fee rate")
    code: Optional[str] = Field(None, description="Acronym identifying the agreed fee")
    amount: Optional[float] = Field(None, description="Monetary value of the fee agreed in the contract")

class LoanPaymentReleaseOverParcel(BaseModel):
    fees: Optional[List[LoanPaymentReleaseOverParcelFee]] = Field(None, description="Fees paid outside the installment")
    charges: Optional[List[LoanPaymentReleaseOverParcelCharge]] = Field(None, description="Charges paid out of installment")

class LoanPaymentRelease(BaseModel):
    isOverParcelPayment: Optional[bool] = Field(None, description="Whether it's a single (true) or scheduled (false) payment")
    installmentId: Optional[str] = Field(None, description="Installment identifier in the institution")
    paidDate: Optional[datetime] = Field(None, description="Date of payment for the contract")
    currencyCode: Optional[str] = Field(None, description="Currency code for the payment (e.g. BRL)")
    paidAmount: Optional[float] = Field(None, description="Payment amount made")
    overParcel: Optional[LoanPaymentReleaseOverParcel] = Field(None, description="Fees/Charges paid outside installment")

class LoanPayments(BaseModel):
    contractOutstandingBalance: Optional[float] = Field(None, description="Amount needed to settle the debt")
    releases: Optional[List[LoanPaymentRelease]] = Field(None, description="List of actual payments made for the loan")

class LoanInstallmentBalloonPaymentAmount(BaseModel):
    value: Optional[float] = Field(None, description="Monetary value of the non-regular installment")
    currencyCode: Optional[str] = Field(None, description="Currency code of the installment, e.g. BRL")

class LoanInstallmentBalloonPayment(BaseModel):
    dueDate: Optional[datetime] = Field(None, description="Expiration date of the non-regular installment")
    amount: Optional[LoanInstallmentBalloonPaymentAmount] = None

class LoanInstallments(BaseModel):
    typeNumberOfInstallments: Optional[str] = Field(None, description="Type of total term (DAY, MONTH, etc.)")
    totalNumberOfInstallments: Optional[int] = Field(None, description="Total term according to the type")
    typeContractRemaining: Optional[str] = Field(None, description="Type of remaining term (DAY, MONTH, etc.)")
    contractRemainingNumber: Optional[int] = Field(None, description="Remaining term according to the type")
    paidInstallments: Optional[int] = Field(None, description="Number of installments paid")
    dueInstallments: Optional[int] = Field(None, description="Number of installments yet to be paid")
    pastDueInstallments: Optional[int] = Field(None, description="Number of overdue installments")
    balloonPayments: Optional[List[LoanInstallmentBalloonPayment]] = Field(None, description="List of non-regular installments")

class LoanWarranty(BaseModel):
    currencyCode: Optional[str] = Field(None, description="Currency of the warranty")
    type: Optional[str] = Field(None, description="Warranty type")
    subtype: Optional[str] = Field(None, description="Warranty subtype")
    amount: Optional[float] = Field(None, description="Warranty original value")

class LoanContractedFinanceCharge(BaseModel):
    type: Optional[str] = Field(None, description="Charge type (e.g. JUROS_REMUNERATORIOS_POR_ATRASO)")
    chargeAdditionalInfo: Optional[str] = Field(None, description="Field for additional info")
    chargeRate: Optional[float] = Field(None, description="Charge value in percentage")

class LoanContractedFee(BaseModel):
    name: Optional[str] = Field(None, description="Name of the agreed fee")
    code: Optional[str] = Field(None, description="Acronym identifying the fee")
    chargeType: Optional[str] = Field(None, description="Charge type (UNICA, BY_INSTALLMENT)")
    charge: Optional[str] = Field(None, description="Billing method (MINIMO, MAXIMO, FIXO, PERCENTUAL)")
    amount: Optional[float] = Field(None, description="Monetary fee value")
    rate: Optional[float] = Field(None, description="Fee rate in percentage")

class LoanInterestRate(BaseModel):
    taxType: Optional[str] = Field(None, description="Tax type (NOMINAL, EFETIVA)")
    interestRateType: Optional[str] = Field(None, description="Interest rate type (SIMPLES, COMPOSTO)")
    taxPeriodicity: Optional[str] = Field(None, description="Tax periodicity (MONTHLY, YEARLY)")
    calculation: Optional[str] = Field(None, description="Calculation basis, e.g. '21/252'")
    referentialRateIndexerType: Optional[str] = Field(None, description="Type of benchmark rate or indexer (PRE_FIXADO, etc.)")
    referentialRateIndexerSubType: Optional[str] = Field(None, description="Subtype of benchmark rate or indexer (TJLP, etc.)")
    referentialRateIndexerAdditionalInfo: Optional[str] = Field(None, description="Additional info about the indexer")
    preFixedRate: Optional[float] = Field(None, description="Pre-fixed rate, if applicable. 1 = 100%")
    postFixedRate: Optional[float] = Field(None, description="Post-fixed rate, if applicable. 1 = 100%")
    additionalInfo: Optional[str] = Field(None, description="Any additional info about the interest rates")

class Loan(BaseModel):
    id: str = Field(..., description="Primary identifier of the loan")
    itemId: str = Field(..., description="Item ID to which this loan belongs")
    contractNumber: Optional[str] = Field(None, description="Contract number given by the institution")
    ipocCode: Optional[str] = Field(None, description="Standard contract number - IPOC code")
    productName: Optional[str] = Field(None, description="Name of the credit operation")
    type: Optional[str] = Field(None, description="Loan type, e.g. CREDITO_PESSOAL_COM_CONSIGNACAO")
    date: Optional[datetime] = Field(None, description="Date the loan data was collected")
    contractDate: Optional[datetime] = Field(None, description="Date when the loan was contracted")
    disbursementDates: Optional[List[datetime]] = Field(None, description="Dates when the loan amount was disbursed")
    settlementDate: Optional[datetime] = Field(None, description="Loan settlement date")
    contractAmount: Optional[float] = Field(None, description="Loan contracted value")
    currencyCode: Optional[str] = Field(None, description="Currency code (e.g. BRL)")
    dueDate: Optional[datetime] = Field(None, description="Loan due date")
    installmentPeriodicity: Optional[str] = Field(None, description="Installments frequency (MONTHLY, etc.)")
    installmentPeriodicityAdditionalInfo: Optional[str] = Field(None, description="Complement info if 'OTHERS'")
    firstInstallmentDueDate: Optional[datetime] = Field(None, description="First installment due date")
    CET: Optional[float] = Field(None, description="Custo Efetivo Total in annual percentage rate")
    amortizationScheduled: Optional[str] = Field(None, description="SAC, PRICE, etc.")
    amortizationScheduledAdditionalInfo: Optional[str] = Field(None, description="Complement if 'OTHERS'")
    cnpjConsignee: Optional[str] = Field(None, description="Consignor CNPJ")
    interestRates: Optional[List[LoanInterestRate]] = Field(None, description="List of loan interest rates")
    contractedFees: Optional[List[LoanContractedFee]] = Field(None, description="List of fees agreed in the contract")
    contractedFinanceCharges: Optional[List[LoanContractedFinanceCharge]] = Field(None, description="List of charges in the contract")
    warranties: Optional[List[LoanWarranty]] = Field(None, description="List of warranties linked to the contract")
    installments: Optional[LoanInstallments] = Field(None, description="Installments data")
    payments: Optional[LoanPayments] = Field(None, description="Loan payments data")


class PageResponseLoans(BaseModel):
    page: int
    total: int
    totalPages: int
    results: List[Loan] = Field(..., description="List of loans")
