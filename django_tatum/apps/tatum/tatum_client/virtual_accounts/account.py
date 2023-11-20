import json

from typing import Any
from typing import Union
from requests import Response

from django_tatum.apps.tatum.tatum_client.exceptions.virtual_account_exceptions import MissingparameterException
from django_tatum.apps.tatum.tatum_client.types.virtual_account_types import AccountQueryDict
from django_tatum.apps.tatum.tatum_client.types.virtual_account_types import CreateAccountXpubDict
from django_tatum.apps.tatum.tatum_client.types.virtual_account_types import BatchAccountDict
from django_tatum.apps.tatum.tatum_client.types.virtual_account_types import CreateAccountDict
from django_tatum.apps.tatum.tatum_client.types.virtual_account_types import UpdateAccountDict
from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import BaseRequestHandler


# TODO: Modify all methods to handle all respnse types
# TODO: Refactor "account/ledger" url prefix to avoid repetition.
# TODO: Error handling


class TatumVirtualAccounts(BaseRequestHandler):
    """Interacting with Tatum Virtual Accounts. See https://apidoc.tatum.io/tag/Account for full docs."""

    def __init__(self):
        """Initialize TatumVirtualAccounts class."""
        self.setup_request_handler("ledger/account")
        super().__init__()

    def _write_json_to_file(
        self,
        filename: str,
        response: Any,
    ):
        """Write the dumped response to a json file.

        Args:
            filename (str): name of the output file.
            response (Any): The response.json object from the response to a request.
        """
        with open(filename, "w") as f:
            json.dump(response, f, indent=4)

    def generate_virtual_account_no_xpub(
        self,
        data: CreateAccountDict,
    ) -> Response:  # sourcery skip: class-extract-method
        """Generate a virtual account without using an extended public key.

        Args:
            data (CreateAccountDict): Params required by
            Tatum API to create a virtual account without an xpub.
            Some are optional, and are marked as such.

            CreateAccountDict is a typed dict with the arguments:
                currency (str): The currency for the virtual account.
                compliant (optional bool): Enable compliant checks. If this is enabled, it is impossible to create \
                    a virtual account if compliant check fails.
                accountCode: (optional str) For bookkeeping to distinct account purpose. 1 - 50 characters.
                accountingCurrency: (optional str)
                accountNumber: (optional str)
                customer: (optional CustomerRegistrationDict): a typed dictionary with the following args:
                    externalId: (required str)
                    accountingCurrency: (optional str)
                    customerCountry: (optional str)
                    providerCountry: (optional str)

            The currency is the only required field. However, if the customer object is specified,
            the externalId of the customer is required and must be specified.

            Args sample:
                data = {
                        "currency": "ETH",
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

        Returns:
            _type_: Response
        """
        if len(data["accountCode"]) > 50:
            raise ValueError("Account code cannot be greater than 50 characters.")
        self.setup_request_handler("ledger/account")
        response = self.Handler.post(data)
        return response.json()

    def generate_virtual_account_with_xpub(
        self,
        data: CreateAccountXpubDict,
    ) -> Response:
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
        self._write_json_to_file(filename="all_virtual_accounts.json", response=response.json())
        return json.dumps(response.json())

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

        self.setup_request_handler(f"ledger/account/{account_id}/balance")
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
        self.setup_request_handler("ledger/account/batch")
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
        customer_id: str,
        account_code: str = None,
        page_size: int = 10,
        offset: int = 0,
    ):
        """Lists all accounts associated with a customer.
        Only active accounts are visible.

        Args:
            customer_id (str): The internal customer ID supplied when creating a virtual account.
            account_code (str, optional): _description_. Defaults to None.
            page_size (int, optional): _description_. Defaults to 10.
            offset (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        self.setup_request_handler(f"ledger/account/customer/{customer_id}")
        self.Handler.headers.pop("Content-Type")
        query: dict = {
            "pageSize": page_size,
        }

        if account_code:
            query["accountCode"] = account_code
        if offset:
            query["offset"] = offset

        response: Response = self.Handler.get(params=query)
        self._write_json_to_file(filename="all_customer_accounts.json", response=response.json())
        return response.json()

    def update_virtual_account(
        self,
        account_id: str,
        account_code: str = None,
        account_number: str = None,
    ):
        """Update the account code or account number from an external system.

        Args:
            account_id (str): The Account ID of the virtual account to be updated. The account ID cannot be updated.
            account_code Optional(str): The new account code to be associated
                with the account ID.
            account_number Optional(str): The new account

        Returns:
            _type_: _description_
        """
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
        Every new blockage has its own distinct ID,
        which is used as a reference.

        When the amount is blocked, it is debited from the available balance
        of the account. The account balance remains the same.
        The account balance represents the total amount of
        funds that are not yet withdrawn or transferred to other accounts.

        The available balance represents the total amount of funds that
        can be used to perform transactions.
        When an account is frozen, the available balance is set to:
        (0 - all blockages applied the account).
        That is, if a blockage of 10 is set to an account with 0 balance,
        the available balance is set to -10.
        The amount can be blocked even if the amount being blocked
        does not exist in the account.

        Args:
            id (str): Account ID
            amount (str): The amount to be blocked on the amount.
            type (str[list[int]]): The type of the blockage to be applied.
                Could be codes or identifiers from you external system.
            description (str, optional): The description of the blockage
                being applied. Defaults to None.

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
        compliant: bool = True,
        transaction_code: str = None,
        payment_id: str = None,
        recipient_note: str = None,
        base_rate: int = 1,
        sender_note: str = None,
    ) -> dict[str, str]:
        """Unblocks a previously blocked amount in an account and invokes a ledger transaction from that
        account to a different recipient. If the request fails, the amount is not unblocked.

        Args:
            blockage_id (str): Blockage ID

            recipientAccountId (str): Recipient account ID within Tatum Platform

            amount (str): Amount to be sent. Amount can be smaller than the blocked amount.

            anonymous (bool, optional): Anonymous transaction does not show sender account to recipient. \
                Defaults to False.

            compliant (bool, optional): Enable compliant checks. The transaction will not be processed \
                if compliant check fails. \
                    Defaults to True.

            transaction_code (str, optional): For bookkeeping to distinct transaction purpose. \
                Defaults to None.

            payment_id (str, optional): Payment ID, External identifier of the payment,\
                which can be used to pair transactions within Tatum accounts. Defaults to None.

            recipient_note (str, optional): A note that will be visible to both sender and recipient. \
                Defaults to None.

            base_rate (int, optional): Exchange rate of the base pair. \
                Only applicable for Tatum's Virtual currencies Ledger transactions. \
                    Override default exchange rate for the Virtual Currency. \
                        Defaults to 1.

            sender_note (str, optional): Note visible to sender. should be between 1 and 500 characters long. \
                Defaults to None.

        Returns:
            dict[str, str]: A dictionary containing the reference to the transaction.
                200 Response Sample:
                {
                    "reference": "0c64cc04-5412-4e57-a51c-ee5727939bcb"
                }
                The reference is a unique identifier of the transaction within the virtual account);\
                    if the transaction fails, you can use this reference to search through the Tatum logs.
        """
        self.setup_request_handler(f"ledger/account/block/{blockage_id}")
        # Only add the optional parameters to the payload if they are supplied
        payload: dict[str, Union[str, bool, int]] = {
            "recipientAccountId": recipientAccountId,
            "amount": amount,
            "anonymous": anonymous,
        }

        if compliant:
            payload["compliant"] = compliant
        else:
            raise ValueError("This transaction will fail because 'compliance' is set to a 'False' value.")
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

    def unblock_amount_in_an_account(
        self,
        blockage_id: str,
    ) -> dict[str, str]:
        """Unblocks a previously blocked amount in an account.
            Increases the available balance in the account where
            the amount was originally blocked.

        Args:
            blockage_id (str): The blocakge ID obtained from a previous amount
                blocking operation.

        Returns:
            dict[str, str]: A dictionary containing the status code and message.
                200 Response Sample:
                    {
                        "message": "Amount unblocked successfully.",
                        "status_code": 200,
                    }
        """
        self.setup_request_handler(f"ledger/account/block/{blockage_id}")
        response: Response = self.Handler.delete()
        if response.status_code == 204:
            response_object: dict[str, str] = {
                "message": "Amount unblocked successfully.",
                "status_code": 204,
            }
            return response_object
        return response.json()

    def get_blocked_amounts_for_an_account(
        self,
        account_id: str,
        page_size: int = 10,
        offset: int = None,
    ):
        """Gets blocked amounts for an account.

        Args:
            account_id (str): The account ID on Tatum.
            page_size (int, optional): How many accounts should be returned in
            a single request. Defaults to 10.
            Max possible value is 50.
            offset (int, optional): Offset to obtain the next page of data.
            Defaults to None, which Tatum interpretes as offset=0.

        Raises:
            ValueError: If a value greater than 50 is passed for page-size,
            a value error is returned to save the user the round trip to Tatum,
            who will eventually return a 400 response :).

        Returns:
            list[dict[str, str]]: An array of blockage ids & blockage details.
                200 Response Sample:
                [
                    {
                        "id": "5e68c66581f2ee32bc354087",
                        "accountId": "5e68c66581f2ee32bc354087",
                        "amount": "5",
                        "type": "DEBIT_CARD_OP",
                        "description": "Card payment in the shop."

                    }
                ]

                id (str): The ID of the blockage
                accountId (str): The ID of the account where the
                                amount is blocked
                amount (str): The amount blocked on the account
                type (str): The type of the blockage supplied when the amount was blocked;
                            This can be a code or an identifier from an external
                            system or a short description of the blockage.
                description (str): The description provided during the blocakge.
        """
        if page_size > 50:
            raise ValueError("Page size cannot be greater than 50.")

        self.setup_request_handler(f"ledger/account/block/{account_id}")
        query: dict = {
            "pageSize": page_size,
        }

        if offset:
            query["offset"] = offset

        response: Response = self.Handler.get(params=query)
        # write the content to a json file
        self._write_json_to_file("blocked_amounts.json", response.json())
        return response.json()

    def get_blocked_amount_by_id(
        self,
        blockage_id: str,
    ) -> dict["str, str"]:
        """Gets blocked amount by id.

        Returns:
            dict[str, str]: The response object from Tatum.
                200 Response Sample:
                {
                    "id": "5e68c66581f2ee32bc354087",
                    "accountId": "5e68c66581f2ee32bc354087",
                    "amount": "5",
                    "type": "DEBIT_CARD_OP",
                    "description": "Card payment in the shop."

                }

                id (str): The ID of the blockage
                accountId (str): The ID of the account where the
                        amount is blocked
                amount (str): The amount blocked on the account
                type (str): The ID of the blockage
                description (str): The ID of the blockage
        """
        self.setup_request_handler(f"ledger/account/block/{blockage_id}/detail")
        response: Response = self.Handler.get()
        return response.json()

    def activate_account(
        self,
        account_id: str,
    ) -> dict[str, Union[str, int]]:
        """Activates an account.

        Args:
            account_id (str): The account ID to be activated.

        Returns:
            dict[str, str]: _description_
        """
        self.setup_request_handler(f"ledger/account/{account_id}/activate")
        response: Response = self.Handler.put()
        if response.status_code == 204:
            response_object: dict[str, str] = {
                "message": "Account activated successfully.",
                "status_code": 200,
            }
            return response_object
        return response.json()

    def deactivate_account(
        self,
        account_id: str,
    ) -> dict[str, Union[str, int]]:
        """Deactivates an account. Only accounts with account and available balances of zero can be deactivated.\
            Accounts with negative balances cannot be deactivated. \
            Deactivated accounts are not visible in the list of accounts, it is not possible to send funds to \
            these accounts or perform transactions. \
            However, they are still present in the ledger as well as all their transaction histories.

        Args:
            account_id (str): The account ID to be deactivated.

        Returns:
            dict[str, str]: _description_
        """
        self.setup_request_handler(f"ledger/account/{account_id}/deactivate")
        response: Response = self.Handler.put()
        if response.status_code == 204:
            response_object: dict[str, Union[str, int]] = {
                "message": "Account deactivated successfully.",
                "status_code": 204,
            }
            return response_object
        print(response.json())
        return response.json()

    def freeze_account(
        self,
        account_id: str,
    ) -> dict[str, Union[str, int]]:
        """Disables all outgoing transactions. \
        Incoming transactions to the account are available.
        When an account is frozen, its available balance is set to 0. Not that a frozen account is still ACTIVE.
        This operation will create a new blockage of type ACCOUNT_FROZEN, which is automatically \
        deleted when the account is unfrozen.

        Args:
            account_id (str): The account ID to be frozen.

        Returns:
            dict[str, str]: _description_
        """
        self.setup_request_handler(f"ledger/account/{account_id}/freeze")
        response: Response = self.Handler.put()
        if response.status_code == 204:
            response_object: dict[str, Union[str, int]] = {
                "message": "Account frozen successfully.",
                "status_code": 204,
            }
            return response_object
        return response.json()

    def unfreeze_account(
        self,
        account_id: str,
    ) -> dict[str, Union[str, int]]:
        """Unfreezes a previously frozen account. \
        This operation will delete the ACCOUNT_FROZEN blockage, \
            which was created when the account was frozen.

        Unfreezing a non-frozen account will not affect the account.

        Args:
            account_id (str): The account ID to be unfrozen.

        Returns:
            dict[str, str]: _description_
        """
        self.setup_request_handler(f"ledger/account/{account_id}/unfreeze")
        response: Response = self.Handler.put()
        if response.status_code == 204:
            response_object: dict[str, Union[str, int]] = {
                "message": "Account unfrozen successfully.",
                "status_code": 204,
            }
            return response_object
        return response.json()


# ---
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
    "currency": "ETH",
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

create_account_with_xpub_payload = {
    "currency": "ETH",
    "xpub": "xpub6FJnrHDNdwdeHxT7eNC3c2oLiCBFg6hezyrzCNrqVXGDHDqsUBbeRdGaFyJxUbqusqAFX6K2ihXJwyCQn1MX3Vrdh1ekUizUkK7PXBEuoCU",
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
    # print(tva.generate_virtual_account_with_xpub(data=create_account_with_xpub_payload))
    # print(tva.list_all_virtual_accounts(list_all_account_payload))
    # print(tva.get_account_entities_count())
    # print(tva.get_account_balance(account_id="6533086644a445035296fe18"))
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

    # print(
    #     tva.unblock_amount_and_perform_transaction(
    #         blockage_id="65386475d8b1ad42ce2af684",
    #         recipientAccountId="6533086644a445035296fe18",
    #         amount="1",
    #     )
    # )  # Not tried this out. TODO: Need to add money from faucets perhaps.
    # print(tva.get_blocked_amounts_for_an_account(account_id="653307d18c610c9e0ef4593f"))
    print(tva.unblock_amount_in_an_account(blockage_id="653efae9f06e25d86dc974d0"))
    # print(tva.get_blocked_amount_by_id(blockage_id="653efae9f06e25d86dc974d0"))
    # print(tva.deactivate_account(account_id="6533086644a445035296fe18"))
    # print(tva.activate_account(account_id="6533086644a445035296fe18"))
    # print(tva.freeze_account(account_id="6533086644a445035296fe18"))
    # print(tva.unfreeze_account(account_id="6533086644a445035296fe18"))

    # print(tva.list_all_customer_accounts(customer_id="653307d18c610c9e0ef45940"))
