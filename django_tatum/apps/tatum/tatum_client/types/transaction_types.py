from typing import TypedDict


class SendPaymentDict(TypedDict, total=False):
    senderAccountId: str
    recipientAccountId: str
    amount: str
    anonymous: bool 
    compliant: bool
    transactionCode: str
    paymentId: str
    recipientNote: str
    senderNote: str
    baseRate: int
    
class TransactionDict(TypedDict, total=False):
    recipientAccountId: str
    amount: str
    anonymous: bool 
    compliant: bool
    transactionCode: str
    paymentId: str
    recipientNote: str
    senderNote: str
    baseRate: int

class BatchPaymentDict(SendPaymentDict):
    senderAccountId: str
    transactions : TransactionDict
    
class AmountDict(TypedDict, total=False):
    op: str
    value: str
    
class FindTransactionDict(TypedDict, total=False):
    id: str
    counterAccount: str 
    sender: int 
    to: int 
    currency: str 
    amount: AmountDict 
    currencies: list 
    transactionType: str 
    opType: str 
    transactionCode: str 
    paymentId: str 
    recipientNote: str 
    senderNote: str

class FindCustomerTransactionDict(TypedDict, total=False):
    customer_id: str 
    account: str
    counterAccount: str 
    sender: int 
    to: int 
    currency: list
    amount: AmountDict 
    currencies: list
    transactionType: str 
    opType: str 
    transactionCode: str 
    paymentId: str 
    recipientNote: str 
    senderNote: str

class FindLedgerTransactionDict(TypedDict, total=False):
    account: str
    counterAccount: str 
    sender: int 
    to: int 
    currency: list
    amount: AmountDict 
    currencies: list
    transactionType: str 
    opType: str 
    transactionCode: str 
    paymentId: str 
    recipientNote: str 
    senderNote: str
    