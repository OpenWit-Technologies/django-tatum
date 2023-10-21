from typing import TypedDict


class AccountQueryDict(TypedDict, total=False):
    page_size: int
    page: int
    sort: str
    sort_by: str
    active: bool
    only_non_zero_balance: bool
    frozen: bool
    currency: str
    account_number: str


class CustomerRegistrationDict(TypedDict, total=False):
    externalId: str
    accountingCurrency: str
    customerCountry: str
    providerCountry: str


class BatchAccountDict(TypedDict, total=False):
    currency: str
    customer: CustomerRegistrationDict
    compliant: bool
    accountCode: str
    account_currency: str
    accountNumber: str
