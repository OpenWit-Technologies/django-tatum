from typing import TypedDict

class UpdateCustomerDict(TypedDict):
    externalId: str
    accountingCurrency: str 
    customerCountry: str 
    providerCountry: str 