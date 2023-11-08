from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import (
    BaseRequestHandler,
)
from django_tatum.apps.tatum.tatum_client.types.transaction_types import (
    SendPaymentDict,
    BatchPaymentDict,
    FindTransactionDict,
    FindCustomerTransactionDict,
    FindLedgerTransactionDict,
)

# from django_tatum.apps.tatum.utils.utility import validate_required_fields

class TatumTransactions(BaseRequestHandler):
    def __init__(self):
        self.setup_request_handler("ledger/transaction")
        super().__init__()
        
    def send_payment(
        self,
        data: SendPaymentDict = None,
    ):  
        """Send a payment transaction.

        Args:
            data (SendPaymentDict): Parameters required by Tatum API to send a payment.
                The structure of SendPaymentDict includes:
                    senderAccountId: str
                    amount: float
                    currency: str
                    paymentId: str
                    recipientNote: str
                    senderNote: str

        Returns:
            Response: The response object containing transaction information.
        """
            
        self.setup_request_handler(f"ledger/transaction")
        response = self.Handler.post(data)
        return response.json()
       

    def send_batch_payment(
        self, 
        data: BatchPaymentDict = None,
    ):
        """Send a batch payment transaction.

        Args:
            data (BatchPaymentDict): Parameters required by Tatum API to send a batch payment.
                The structure of BatchPaymentDict includes:
                    payments: List[SendPaymentDict]

        Returns:
            Response: The response object containing transaction information.
        """
        return self.extracted_from_send_payment(
            "ledger/transaction/batch", data
        )


    def find_transaction_for_account(
        self,
        data: FindTransactionDict = None,
        pageSize: int = None,
        offset: int = None,
        count: bool = None,
    ):
        """Find transactions for a specific account.

        Args:
            data (FindTransactionDict): Parameters required by Tatum API to find transactions for an account.
                The structure of FindTransactionDict includes various optional parameters.
            pageSize (int): The number of transactions to retrieve per page.
            offset (int): The offset for paginating through transactions.
            count (bool): If True, include the total count of transactions in the response.

        Returns:
            Response: The response object containing transaction information.
        """
        
        try:
            self.setup_request_handler(f"ledger/transaction/account")
            
            # if "id" not in data or data["id"] is None:
            #     raise ValueError("Missing 'id' field in data")

            query = {}

            if data:
                query |= data
                
            # if pageSize, offset, count are specified, then append them to query dictionary
            if pageSize:
                query["pageSize"] = pageSize
            if offset:
                query["offset"] = offset
            if count:
                query["count"] = count
                
            response = self.Handler.post(params=query)
            return response.json()
        
        
        except Exception as e:
            return {
                "error": "An error occured while trying to send payment",
                "details": str(e),
            }

    def find_transaction_accross_all_customer_accounts(
        self,
        data: FindCustomerTransactionDict = None,
        pageSize: int = None,
        offset: int = None,
        count: bool = None,
    ):
        """Find transactions across all customer accounts.

        Args:
            data (FindCustomerTransactionDict): Parameters required by Tatum API to find transactions across all customer accounts.
                The structure of FindCustomerTransactionDict includes various optional parameters.
            pageSize (int): The number of transactions to retrieve per page.
            offset (int): The offset for paginating through transactions.
            count (bool): If True, include the total count of transactions in the response.



        Returns:
            Response: The response object containing transaction information.
        """        
        
        try:
            self.setup_request_handler(f"ledger/transaction/customer")
            
            # if "id" not in data or data["id"] is None:
            #     raise ValueError("Missing 'id' field in data")

            query = {}

            if data:
                query |= data
                
            # if pageSize, offset, count are specified, then append them to query dictionary
            if pageSize:
                query["pageSize"] = pageSize
            if offset:
                query["offset"] = offset
            if count:
                query["count"] = count
                
            response = self.Handler.post(params=query)
            return response.json()
        
        except Exception as e:
            return {
                "error": "An error occured while trying to send payment",
                "details": str(e),
            }
        
        

    def find_transaction_within_ledger(
        self,
        data: FindLedgerTransactionDict = None,
        pageSize: int = None,
        offset: int = None,
        count: bool = None,
    ):
        """Find transactions within a ledger.

        Args:
            data (FindLedgerTransactionDict): Parameters required by Tatum API to find transactions within a ledger.
                The structure of FindLedgerTransactionDict includes various optional parameters.
            pageSize (int): The number of transactions to retrieve per page.
            offset (int): The offset for paginating through transactions.
            count (bool): If True, include the total count of transactions in the response.


        Returns:
            Response: The response object containing transaction information.
        """
        
        try:
            self.setup_request_handler(f"ledger/transaction/ledger")
            
            # if "id" not in data or data["id"] is None:
            #     raise ValueError("Missing 'id' field in data")

            query = {}

            if data:
                query |= data
                
            # if pageSize, offset, count are specified, then append them to query dictionary
            if pageSize:
                query["pageSize"] = pageSize
            if offset:
                query["offset"] = offset
            if count:
                query["count"] = count
                
            response = self.Handler.post(params=query)
            return response.json()
        
        except ValueError as e:
            return {
                "error": "Validation Error",
                "details": str(e),
            }
        
        except Exception as e:
            return {
                "error": "An error occured while trying to send payment",
                "details": str(e),
            }
            
    def find_transaction_by_reference(
        self, 
        reference_id: str,
    ):
        """Find a transaction by its reference ID.

        Args:
            reference_id (str): The reference ID of the transaction to be found.

        Returns:
            Response: The response object containing transaction information.
        """
        
        self.setup_request_handler(f"ledger/transaction/reference/{reference_id}")
      
        response = self.Handler.get()
        return response.json()
            

    
    
send_payment_payload = {
    "senderAccountId": "62fd4871427463ab2ba57af5",
    "recipientAccountId": "62f6a23156e369804d2b3490",
    "amount": "0.1",
    "anonymous": False,  
    "compliant": True,
    "transactionCode": "123456789",
    "paymentId": "987654321",
    "recipientNote": "Send",
    "senderNote": None,
    "baseRate": 1,
}

send_batch_payment_payload = {
    "senderAccountId": "62fd4871427463ab2ba57af5",
    "transaction": [
        {
            "recipientAccountId": "62f6a23156e369804d2b3490",
            "amount": "0.1",
            "anonymous": False,  
            "compliant": True,
            "transactionCode": "123456789",
            "paymentId": "987654321",
            "recipientNote": "Send",
            "senderNote": None,
            "baseRate": 1,  
        }
    ]
}

find_transaction_for_account_payload = {
    "id": "62f6a23156e369804d2b3490",
    "counterAccount": "62f6a23156e369804d2b3490",
    "from": None,
    "to": None,
    "currency": "Matic",
    "amount": [
        {
           "op": "lte",
           "value": "0.1" ,
        }
    ],
    "currencies": "Matic",
    "transactionType": "SEND_PAYMENT",
    "opType": "PAYMENT",
    "transactionCode": "123456789",
    "paymentId": "987654321",
    "recipientNote": "Send",
    "senderNote": None,
    "pageSize":  "10",
    "offset": "0",
    "count": True,
}

find_transaction_accross_all_customer_accounts_payload = {
    "id": "62fd4871427463ab2ba57af5",
    "account": "123456789",
    "counterAccount": "62f6a23156e369804d2b3490",
    "sender": None,
    "to": None,
    "currency": "Matic",
    "amount": [
        {
           "op": "lte",
           "value": "0.1" ,
        }
    ],
    "currencies": "Matic",
    "transactionType": "SEND_PAYMENT",
    "opType": "PAYMENT",
    "transactionCode": "123456789",
    "paymentId": "987654321",
    "recipientNote": "Send",
    "senderNote": None,
    "pageSize":  "10",
    "offset": "0",
    "count": True,
}

find_transaction_within_ledger_payload = {
    "account": "123456789",
    "counterAccount": "62f6a23156e369804d2b3490",
    "sender": None,
    "to": None,
    "currency": "Matic",
    "amount": [
        {
           "op": "lte",
           "value": "0.1" ,
        }
    ],
    "currencies": "Matic",
    "transactionType": "SEND_PAYMENT",
    "opType": "PAYMENT",
    "transactionCode": "123456789",
    "paymentId": "987654321",
    "recipientNote": "Send",
    "senderNote": None,
    "pageSize":  "10",
    "offset": "0",
}


if __name__ == "__main__":
    tat = TatumTransactions()
    # print(tat.send_payment(data=send_payment_payload))
    # print(tat.send_batch_payment(data=send_batch_payment_payload))
    # print(tat.find_transaction_for_account(data=find_transaction_for_account_payload))
    # print(tat.find_transaction_accross_all_customer_accounts(data=find_transaction_accross_all_customer_accounts_payload))
    # print(tat.find_transaction_within_ledger(data=find_transaction_within_ledger_payload))
    # print(tat.find_transaction_by_reference(reference_id="2a0786b8-52ef-44c1-a582-4f7e3c748c08"))  
    