from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class BenefitLoanClient(BaseModel):
    document: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    addressStreet: Optional[str] = None
    addressNumber: Optional[str] = None
    addressCity: Optional[str] = None
    addressZipCode: Optional[str] = None
    addressState: Optional[str] = None

class BenefitLoan(BaseModel):
    contractCode: Optional[str] = None
    hisconContractCode: Optional[str] = None
    effectiveInterestRate: Optional[float] = None
    cetAnnualRate: Optional[float] = None
    cetMonthRate: Optional[float] = None
    currencyCode: Optional[str] = None
    amortizationRegime: Optional[str] = None
    operationHiringDate: Optional[datetime] = None
    installmentsQuantity: Optional[int] = None
    installmentsValue: Optional[float] = None
    dueDateFirstInstallment: Optional[datetime] = None
    dueDateLastInstallment: Optional[datetime] = None
    cnpjCorrespondentBanking: Optional[str] = None
    pdfContract: Optional[str] = None
    client: Optional[BenefitLoanClient] = None

class PayingInstitution(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    agency: Optional[str] = None
    account: Optional[str] = None

class Benefit(BaseModel):
    id: str
    itemId: str
    number: Optional[str] = None
    type: Optional[str] = None
    beneficiaryName: Optional[str] = None
    marginBaseValue: Optional[float] = None
    availableMarginValue: Optional[float] = None
    usedMarginValue: Optional[float] = None
    reservedMarginValue: Optional[float] = None
    deductibleAvailableMarginValue: Optional[float] = None
    payingInstitution: Optional[PayingInstitution] = None
    loans: Optional[List[BenefitLoan]] = None

class PageResponseBenefits(BaseModel):
    page: int
    total: int
    totalPages: int
    results: List[Benefit]

