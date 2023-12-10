"""These endpoints are used to create and list transactions within Tatum Private Ledger.
These transactions are performed between 2 accounts with the same currency.
To perform an exchange operation between accounts with different currencies,
use the 'Order Book' API calls."""
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
from django_tatum.apps.tatum.utils.response_handlers import handle_response_object

# from django_tatum.apps.tatum.utils.utility import validate_required_fields


class TatumTransactions(BaseRequestHandler):
    """Tatum Private Ledger supports microtransactions - a transaction of an amount as little as 1e-30 (30 decimal places).
    Transactions are atomic.
    When there is an insufficient balance in the sender account, or recipient account cannot receive funds,
    the transaction is not settled."""

    def __init__(self):
        self.setup_request_handler("ledger/transaction")
        super().__init__()

    def send_payment(
        self,
        sender_account_id: str,
        recipient_account_id: str,
        amount: str,
        anonymous: bool = False,
        compliant: bool = True,
        transaction_code: str = None,
        payment_id: str = None,
        recipient_note: str = None,
        base_rate: int = 1,
        sender_note: str = None,
    ):
        """Send payments within the TATUM PRIVATE ledger. All assets are settled instantly.
         This method is only used for transferring assets between accounts within Tatum and
         will not send any funds to blockchain addresses.

         When a transaction is settled, 2 transaction records are created,
         1 for each of the participants.
         These 2 records are connected via a transaction reference, which is the same for both of them.

        Args:
            sender_account_id (str): Internal sender account ID within Tatum platform.
            recipient_account_id (str): Internal recipient account ID within Tatum platform
            amount (str): Amount to be sent.
            anonymous (bool, optional): Anonymous transaction does not show sender account to recipient.
                Defaults to false
            compliant (bool, optional): Enable compliant checks. Transaction will not be processed, if compliant check fails.
                Defaults to None.
            transaction_code (str, optional): For bookkeeping to distinct transaction purpose.
                Defaults to None.
            payment_id (str, optional): Payment ID, External identifier of the payment,
                which can be used to pair transactions within Tatum accounts.
                Defaults to None.
            recipient_note (str, optional): Note visible to both, sender and recipient.
                Defaults to None.
            base_rate (int, optional): Exchange rate of the base pair.
                Only applicable for Tatum's Virtual currencies Ledger transactions.
                Override default exchange rate for the Virtual Currency.
                Defaults to 1.
            sender_note (str, optional): Note visible to sender.
                Defaults to None.

        Returns:
            _type_: JSON object containing the internal reference to the transaction (a unique identifier of
                the transaction within the virtual account);
                if the transaction fails, use this reference to search through the logs.
        """

        self.setup_request_handler("ledger/transaction")
        data: SendPaymentDict = {
            "senderAccountId": sender_account_id,
            "recipientAccountId": recipient_account_id,
            "amount": amount,
        }
        if anonymous:
            data["anonymous"] = anonymous
        if compliant:
            data["compliant"] = compliant
        if transaction_code:
            data["transactionCode"] = transaction_code
        if payment_id:
            data["paymentId"] = payment_id
        if recipient_note:
            data["recipientNote"] = recipient_note
        if base_rate:
            data["baseRate"] = base_rate
        if sender_note:
            data["senderNote"] = sender_note

        response = handle_response_object(self.Handler.post(data))
        return response.json()

    def send_batch_payment(
        self,
        data: BatchPaymentDict = None,
    ):
        """Sends the 'N' payments within Tatum Private Ledger. All assets are settled instantly.

        Args:
            data (BatchPaymentDict): Parameters required by Tatum API to send a batch payment.
                The structure of BatchPaymentDict includes:
                    payments: List[SendPaymentDict]

        Returns:
            Response: The response object containing transaction information.
        """
        self.setup_request_handler("ledger/transaction/batch")
        response = self.Handler.post(data)

        return response.json()

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
            self.setup_request_handler("ledger/transaction/account")

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
            data (FindCustomerTransactionDict): Parameters required by Tatum API to find
                transactions across all customer accounts.
            The structure of FindCustomerTransactionDict includes various optional parameters.
            pageSize (int): The number of transactions to retrieve per page.
            offset (int): The offset for paginating through transactions.
            count (bool): If True, include the total count of transactions in the response.



        Returns:
            Response: The response object containing transaction information.
        """

        try:
            self.setup_request_handler("ledger/transaction/customer")

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
            self.setup_request_handler("ledger/transaction/ledger")

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
    ],
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
            "value": "0.1",
        }
    ],
    "currencies": "Matic",
    "transactionType": "SEND_PAYMENT",
    "opType": "PAYMENT",
    "transactionCode": "123456789",
    "paymentId": "987654321",
    "recipientNote": "Send",
    "senderNote": None,
    "pageSize": "10",
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
            "value": "0.1",
        }
    ],
    "currencies": "Matic",
    "transactionType": "SEND_PAYMENT",
    "opType": "PAYMENT",
    "transactionCode": "123456789",
    "paymentId": "987654321",
    "recipientNote": "Send",
    "senderNote": None,
    "pageSize": "10",
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
            "value": "0.1",
        }
    ],
    "currencies": "Matic",
    "transactionType": "SEND_PAYMENT",
    "opType": "PAYMENT",
    "transactionCode": "123456789",
    "paymentId": "987654321",
    "recipientNote": "Send",
    "senderNote": None,
    "pageSize": "10",
    "offset": "0",
}


if __name__ == "__main__":
    tat = TatumTransactions()
    print(tat.send_payment(data=send_payment_payload))
    # print(tat.send_batch_payment(data=send_batch_payment_payload))
    # print(tat.find_transaction_for_account(data=find_transaction_for_account_payload))
    # print(tat.find_transaction_accross_all_customer_accounts(data=find_transaction_accross_all_customer_accounts_payload))
    # print(tat.find_transaction_within_ledger(data=find_transaction_within_ledger_payload))
    # print(tat.find_transaction_by_reference(reference_id="2a0786b8-52ef-44c1-a582-4f7e3c748c08"))
