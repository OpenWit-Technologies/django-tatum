from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler
import django_tatum.apps.tatum as utils


class TatumTransactions():
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}ledger/transaction"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def send_payment(
        self,
        senderAccountId: str,
        recipientAccountId: str,
        amount: str,
        anonymous: bool = False,
        compliant: bool = False,
        transactionCode: str = None,
        paymentId: str = None,
        recipientNote: str = None,
        senderNote: str = None,
        baseRate: int = 1,
    ):

        data = utils.validate_required_fields(
            {
                "senderAccountId": senderAccountId,
                "recipientAccountId": recipientAccountId,
                "amount": amount,
            }
        )

        try:
            if anonymous:
                data["anonymous"] = anonymous
            if compliant:
                data["compliant"] = compliant
            if transactionCode:
                data["transactionCode"] = transactionCode
            if paymentId:
                data["paymentId"] = paymentId
            if recipientNote:
                data["recipientNote"] = recipientNote
            if senderNote:
                data["senderNote"] = senderNote
            if baseRate and baseRate >= 1:
                data["baseRate"] = baseRate
            else:
                return "Base rate must be greater than or equal to 1"

            response = self.Handler.post(data)
            return response.json()

        except Exception as e:
            return {
                "error": "An error occured while trying to send payment",
                "details": str(e),
            }

    # def send_batch_payment(self, data: list):
    #     pass

    def find_transaction_for_account(
        self,
        id: str,
        pageSize: int = None,
        offset: int = None,
        count: bool = None,
        counterAccount: str = None,
        sender: int = None,
        to: int = None,
        currency: str = None,
        amount: list = None,
        currencies: list = None,
        transactionType: str = None,
        transactionTypes: list = None,
        opType: str = None,
        transactionCode: str = None,
        paymentId: str = None,
        recipientNote: str = None,
        senderNote: str = None,
    ):

        requestUrl = f"{creds.TATUM_BASE_URL}ledger/transaction/account"
        Handler = RequestHandler(
            requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )
        query = {}
        # if pageSize, offset, count are specified, then append them to query dictionary
        if pageSize:
            query["pageSize"] = pageSize
        if offset:
            query["offset"] = offset
        if count:
            query["count"] = count
        if not (
            data := utils.validate_required_fields(
                {
                    "id": id,
                }
            )
        ):
            return "You must specify at least the id of the account."

        try:
            if counterAccount and counterAccount is not None:
                data["counterAccount"] = counterAccount
            if sender:
                data["from"] = sender
            if to:
                data["to"] = to
            if currency:
                data["currency"] = currency
            if amount:
                if len(amount) != 2:
                    return "Amount is not a required field, but if you choose to specify it, it must be a list of two values: ['op', 'value']."
                if (amount["op"] in ["gt", "gte", "lt", "lte", "eq", "neq"]) and (
                    amount["value"] is not None
                ):
                    data["amount"] = amount
                else:
                    return {
                        "error": "Invalid amount query",
                        "detail": "Amount must be a list of two items. The first item must be a string of either of the following: 'gt', 'gte', 'lt', 'lte', 'eq', 'neq', and the second item must be a string indicating the value of the operation.",
                    }
            if currencies:
                data["currencies"] = currencies
            if transactionType:
                data["transactionType"] = transactionType
            if transactionTypes and transactionTypes is not None:
                data["transactionTypes"] = transactionTypes
            if opType:
                data["opType"] = opType
            if transactionCode:
                data["transactionCode"] = transactionCode
            if paymentId:
                data["paymentId"] = paymentId
            if recipientNote:
                data["recipientNote"] = recipientNote
            if senderNote:
                data["senderNote"] = senderNote

        except Exception as e:
            return {
                "error": "An error occured while trying to find transaction for account",
                "details": str(e),
            }

    def find_transaction_accross_all_customer_accounts(
        self,
        pageSize: int = None,
        offset: int = None,
        count: bool = None,
        id: str = None,
        counterAccount: str = None,
        startDate: int = None,
        to: int = None,
        currency: str = None,
        amount: list = None,
        currencies: list = None,
        transactionType: list = None,
        opType: str = None,
        transactionCode: str = None,
        paymentId: str = None,
        recipientNote: str = None,
        senderNote: str = None,
    ):

        requestUrl = f"{creds.TATUM_BASE_URL}ledger/transaction/customer"
        Handler = RequestHandler(
            requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )
        query = {}
        # if pageSize, offset, count are specified, then append them to query dictionary
        if pageSize:
            query["pageSize"] = pageSize
        if offset:
            query["offset"] = offset
        if count:
            query["count"] = count
        if not (
            data := utils.validate_required_fields(
                {
                    "id": id,
                }
            )
        ):
            return "You must specify at least the id of the account."
        try:
            if counterAccount:
                data["counterAccount"] = counterAccount
            if startDate:
                data["startDate"] = startDate
            if to:
                data["to"] = to
            if currency:
                data["currency"] = currency
            if amount:
                data["amount"] = amount
            if transactionType:
                data["transactionType"] = currencies
            if opType:
                data["opType"] = opType
            if transactionCode:
                data["transactionCode"] = transactionCode
            if paymentId:
                data["paymentId"] = paymentId
            if recipientNote:
                data["recipientNote"] = recipientNote
            if senderNote:
                data["senderNote"] = senderNote

            response = Handler.post(data, params=query)
            return response.json()

        except Exception as e:
            return {
                "error": "An error occured while trying to find transaction for account",
                "details": str(e),
            }

    def find_transaction_within_ledger(
        self,
        pageSize: int = None,
        offset: int = None,
        count: bool = None,
        account: str = None,
        counterAccount: str = None,
        currency: str = None,
        startDate: int = None,  # represents 'from' on tatum's side
        amount: list = None,
        to: int = None,
        currencies: list = None,
        transactionType: str = None,
        transactionTypes: list = None,
        opType: str = None,
        transactionCode: str = None,
        paymentId: str = None,
        recipientNote: str = None,
        senderNote: str = None,
    ):
        requestUrl = f"{creds.TATUM_BASE_URL}ledger/transaction/ledger"
        Handler = RequestHandler(
            requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )
        query = {}
        # if pageSize, offset, count are specified, then append them to query dictionary
        if pageSize:
            query["pageSize"] = pageSize
        if offset:
            query["offset"] = offset
        if count:
            query["count"] = count
        if not (
            data := utils.validate_required_fields(
                {
                    "account": account,
                }
            )
        ):
            return "You must specify at least the id of the account."
        try:
            if counterAccount:
                data["counterAccount"] = counterAccount
            if startDate:
                data["startDate"] = startDate
            if to:
                data["to"] = to
            if currency:
                data["currency"] = currency
            if amount:
                data["amount"] = amount
            if transactionType:
                data["transactionType"] = currencies
            if opType:
                data["opType"] = opType
            if transactionCode:
                data["transactionCode"] = transactionCode
            if paymentId:
                data["paymentId"] = paymentId
            if recipientNote:
                data["recipientNote"] = recipientNote
            if senderNote:
                data["senderNote"] = senderNote
            if transactionTypes:
                data["transactionTypes"] = transactionTypes

            response = Handler.post(data, params=query)
            return response.json()

        except Exception as e:
            return {
                "error": "An error occured while trying to find transaction for account",
                "details": str(e),
            }

    def find_transaction_by_reference(self, reference):
        requestUrl = f"{creds.TATUM_BASE_URL}ledger/transaction/reference/{reference}"
        Handler = RequestHandler(
            self.requestUrl,
            {"x-api-key": creds.TATUM_API_KEY},
        )

        response = Handler.get()
        return response.json()
    
