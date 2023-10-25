import json
from typing import Any, Union

from requests import Response
from django_tatum.apps.tatum.tatum_client.exceptions.virtual_account_exceptions import (
    MissingparameterException,
)

# from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.tatum_client.types.virtual_account_types import (
    AccountQueryDict,
    BatchAccountDict,
    CreateAccountDict,
    UpdateAccountDict,
)
from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import (
    BaseRequestHandler,
)


class TatumVirtualAccounts(BaseRequestHandler):
    def __init__(self):
        self.setup_request_handler("ledger/account")
        super().__init__()

    def generate_virtual_account_no_xpub(
        self,
        data: CreateAccountDict,
    ) -> Response:
        """Generate a virtual account without using an extended public key.

        Args:
            data (CreateAccountDict): Params required by
            Tatum API to create a virtual account without an xpub.
            Some are optional.
            They include:
                currency: str
                customer: CustomerRegistrationDict
                compliant: bool
                accountCode: str
                accountingCurrency: str
                accountNumber: str

            The currency is the only required field.
            However, if the customer object is specified,
            the externalId of the customer is required.

        Returns:
            _type_: Response
        """
        self.setup_request_handler("ledger/account")
        response = self.Handler.post(data)
        return response.json()

    def list_all_virtual_accounts(
        self,
        query: AccountQueryDict = None,
    ) -> Response:
        self.setup_request_handler("ledger/account")
        if query is None:
            query = {}

        # Define the expected query parameters and their types
        expected_params = {
            "page_size": int,
            "page": int,
            "sort": str,
            "sort_by": str,
            "active": bool,
            "only_non_zero_balance": bool,
            "frozen": bool,
            "currency": str,
            "account_number": str,
        }

        # Validate the provided query parameters
        for param, param_type in query.items():
            if param not in expected_params:
                raise ValueError(f"Invalid query parameter '{param}'")
            if not isinstance(param_type, expected_params[param]):
                raise ValueError(f"Invalid type for query parameter '{param}'")

        response = self.Handler.get(params=json.dumps(query))
        return json.jumps(response.json())

    def get_account_entities_count(
        self,
        query: AccountQueryDict = None,
    ) -> str:
        """Count of accounts that were found from /v3/ledger/account.

        Args:
            query (AccountQueryDict, optional): Accepted payload dict.
            Defaults to None.

        Returns:
            _type_: JSON serialized string.
        """
        if query is None:
            query = {}
        self.setup_request_handler("ledger/account/count")
        response = self.Handler.get(
            params=query,
        )
        return json.dumps(response.json())

    def get_account_balance(self, account_id: str):
        if account_id is None:
            return f"MissingParameterErrror. {account_id} must be specified."

        self.setup_request_handler(f"ledger/{account_id}/balance")
        response = self.Handler.get()
        return response.json()

    def get_account_by_id(
        self,
        account_id: str,
    ) -> dict[str, str]:
        if account_id is None:
            raise MissingparameterException([account_id], "Missing parameter.")

        self.setup_request_handler(f"ledger/account/{account_id}")
        response = self.Handler.get()
        return response.json()

    def create_batch_accounts(
        self,
        accounts: list[BatchAccountDict],
    ):
        self.setup_request_handler("ledger/batch")
        payload: dict[str, Any] = {
            "accounts": accounts,
        }
        response = self.Handler.post(
            data=payload,
        )
        print(response.json())
        return response.json()

    def list_all_customer_accounts(
        self,
        account_id: str,
        account_code: str = None,
        page_size: int = 10,
        offset: int = 0,
    ):
        self.setup_request_handler(f"ledger/account/customer/{account_id}")
        self.Handler.headers.pop("Content-Type")
        query: dict = {
            "pageSize": page_size,
        }

        if account_code:
            query["accountCode"] = account_code
        if offset:
            query["offset"] = offset

        response: Response = self.Handler.get(params=query)
        print(response)
        return response.json()

    def update_virtual_account(
        self,
        account_id: str,
        account_code: str,
        account_number: str,
    ):
        self.setup_request_handler(f"ledger/account/{account_id}")
        payload: UpdateAccountDict = {
            "id": account_id,
            "accountCode": account_code,
            "accountNumber": account_number,
        }

        response: Response = self.Handler.put(
            data=payload,
        )
        print(response)
        return response

    def block_amount_in_account(
        self,
        id: str,
        amount: str,
        type: list[int],
        description: str = None,
    ):
        """Blocks an amount in an account.
        Any number of distinct amounts can be blocked in one account.
        Every new blockage has its own distinct ID, which is used as a reference.
        When the amount is blocked, it is debited from the available balance of the account.
        The account balance remains the same.
        The account balance represents the total amount of funds in the account.
        The available balance represents the total amount of funds that can be used to perform transactions.
        When an account is frozen, the available balance is set to 0 minus all blockages for the account.

        The amount can be blocked even if the amount supplied does not exist in the account.

        Args:
            id (str): Account ID
            amount (str): The amount to be blocked on the amount.
            type (str[list[int]]): The type of the blockage that you are applying.

                Could be codes or identifiers from you external system.
            description (str, optional): The description of the blockage that you are applying.
                Defaults to None.

        Returns:
            _type_: _description_
        """
        self.setup_request_handler(f"ledger/account/block/{id}")
        payload: dict[str, Union[str, list]] = {
            "amount": amount,
            "type": str(type),
        }
        if description:
            payload["description"] = description
        response: Response = self.Handler.post(
            data=payload,
        )

        return response.json()

    def unblock_amount_and_perform_transaction(
        self,
        blockage_id: str,
        recipientAccountId: str,
        amount: str,
        anonymous: bool = False,
        compliant: bool = None,
        transaction_code: str = None,
        payment_id: str = None,
        recipient_note: str = None,
        base_rate: int = None,
        sender_note: str = None,
    ):
        self.setup_request_handler(f"ledger/account/block/{blockage_id}")
        # Only add the optional parameters to the payload if they are supplied
        payload: dict[str, Union[str, bool, int]] = {
            "recipientAccountId": recipientAccountId,
            "amount": amount,
            "anonymous": anonymous,
        }

        if compliant:
            payload["compliant"] = compliant
        if transaction_code:
            payload["transactionCode"] = transaction_code
        if payment_id:
            payload["paymentId"] = payment_id
        if recipient_note:
            payload["recipientNote"] = recipient_note
        if base_rate:
            payload["baseRate"] = base_rate
        if sender_note:
            payload["senderNote"] = sender_note

        response: Response = self.Handler.put(
            data=payload,
        )

        if response.status_code != 200:
            content = json.loads(response.content)
            content.pop("dashboardLog")
            return content
        return response.json()


creatr_bulk_account_payload = {
    "accounts": [
        {
            "currency": "BTC",
            "customer": {
                "externalId": "123456789",
                "accountingCurrency": "USD",
                "customerCountry": "US",
                "providerCountry": "US",
            },
            "compliant": True,
            "accountCode": "123456789",
            "accountingCurrency": "USD",
            "accountNumber": "123456789",
        },
    ]
}

create_account_payload = {
    "currency": "BTC",
    "customer": {
        "externalId": "123456789",
        "accountingCurrency": "USD",
        "customerCountry": "US",
        "providerCountry": "US",
    },
    "compliant": True,
    "accountCode": "123456789",
    "accountingCurrency": "USD",
    "accountNumber": "123456789",
}

block_account_payload = {
    "amount": "10",
    "type": ["1223"],
}


list_all_account_payload = {"active": True}

if __name__ == "__main__":
    tva = TatumVirtualAccounts()
    # print(tva.generate_virtual_account_no_xpub(data=create_account_payload))
    # print(tva.list_all_virtual_accounts(list_all_account_payload))
    # print(tva.get_account_entities_count())
    # print(tva.get_account_balance(account_id="0x1c0a4c3c7a3e2c6a1b3d6c4b7b3f9b7c9b1c0a4c3c7a3e2c6a1b3d6c4b7b3f9b7c9"))
    # print(tva.create_batch_accounts(accounts=creatr_bulk_account_payload["accounts"]))
    # print(tva.list_all_customer_accounts(account_id="653307d18c610c9e0ef45940"))

    # print(
    #     tva.update_virtual_account(
    #         account_code="013791914",
    #         account_id="653307d18c610c9e0ef4593f",
    #         account_number="0137492934",
    #     )
    # )

    # print(tva.get_account_by_id("653307d18c610c9e0ef4593f"))

    # print(
    #     tva.block_amount_in_account(
    #         "653307d18c610c9e0ef4593f",
    #         block_account_payload["amount"],
    #         block_account_payload["type"],
    #     )
    # )

    print(
        tva.unblock_amount_and_perform_transaction(
            blockage_id="65386475d8b1ad42ce2af684",
            recipientAccountId="6533086644a445035296fe18",
            amount="1",
        )
    ) # Not tried this out. TODO: Need to add money from faucets perhaps.

