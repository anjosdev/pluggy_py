from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class PhoneNumber(BaseModel):
    type: Optional[str] = Field(None, description="Type of phone number: personal, work, or residential")
    value: str = Field(..., description="The complete phone number")

class Email(BaseModel):
    type: Optional[str] = Field(None, description="Type of email: personal or work")
    value: str = Field(..., description="The full email of the person")

class Address(BaseModel):
    fullAddress: Optional[str] = Field(None, description="Full address using all components available")
    primaryAddress: Optional[str] = Field(None, description="Primary address, street name and number")
    city: Optional[str] = Field(None, description="City name")
    postalCode: Optional[str] = Field(None, description="Zip code")
    state: Optional[str] = Field(None, description="State or province")
    country: Optional[str] = Field(None, description="Country name")
    type: Optional[str] = Field(None, description="Type of address, Personal or Work")

class IdentityRelation(BaseModel):
    type: Optional[str] = Field(None, description="Relation type: Father, Mother, or Spouse")
    name: Optional[str] = Field(None, description="Full name of the related person")
    document: Optional[str] = Field(None, description="Primary document of the related person")

class InformedIncome(BaseModel):
    frequency: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None

class InformedPatrimony(BaseModel):
    amount: Optional[float] = None
    year: Optional[int] = None

class Qualifications(BaseModel):
    companyCnpj: str
    occupationCode: Optional[str] = None
    informedIncome: Optional[InformedIncome] = None
    informedPatrimony: Optional[InformedPatrimony] = None

class Procurator(BaseModel):
    type: Optional[str] = None
    cpfNumber: Optional[str] = None
    civilName: Optional[str] = None
    socialName: Optional[str] = None

class FinancialRelationshipsAccounts(BaseModel):
    compeCode: Optional[str] = None
    branchCode: Optional[str] = None
    number: Optional[str] = None
    checkDigit: Optional[str] = None
    type: Optional[str] = None
    subtype: Optional[str] = None

class FinancialRelationships(BaseModel):
    startDate: Optional[datetime] = None
    productsServicesType: Optional[List[str]] = None
    procurators: List[Procurator] = Field(default_factory=list)
    accounts: Optional[List[FinancialRelationshipsAccounts]] = None

class Identity(BaseModel):
    id: str = Field(..., description="The ID of the identity to retrieve")
    itemId: str = Field(..., description="UUID of the item linked to the identity")
    birthDate: Optional[datetime] = Field(None, description="Date of birth")
    taxNumber: Optional[str] = None
    document: Optional[str] = None
    documentType: Optional[str] = None
    jobTitle: Optional[str] = None
    fullName: Optional[str] = None
    establishmentCode: Optional[str] = None
    establishmentName: Optional[str] = None
    companyName: Optional[str] = None
    phoneNumbers: Optional[List[PhoneNumber]] = None
    emails: Optional[List[Email]] = None
    addresses: Optional[List[Address]] = None
    relations: Optional[List[IdentityRelation]] = None
    investorProfile: Optional[str] = None
    qualifications: Optional[Qualifications] = None
    financialRelationships: Optional[FinancialRelationships] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
