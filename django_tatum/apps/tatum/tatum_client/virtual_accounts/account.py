from typing import Any
from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.tatum_client.types.virtual_account_types import (
    AccountQueryDict,
    BatchAccountDict,
)
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class TatumVirtualAccounts:
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}ledger/account"
        self.Handler = RequestHandler(
            url=self.requestUrl,
            headers={
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def generate_virtual_account(self, data: dict):
        response = self.Handler.post(data)
        return response.json()

    def list_all_virtual_accounts(
        self,
        query: AccountQueryDict = None,
    ):
        if query is None:
            query = {}
        response = self.Handler.get(params=query)
        return response.json()

    def get_account_entities_count(
        self,
        query: AccountQueryDict = None,
    ):
        if query is None:
            query = {}
        self.Handler.url = f"{self.requestUrl}/count"
        response = self.Handler.get(
            params=query,
        )
        return response.json()

    def get_account_balance(self, account_id: str):
        if account_id is None:
            return f"MissingParameterErrror. {account_id} must be specified."

        self.Handler.url = f"{self.requestUrl}/{account_id}/balance"
        response = self.Handler.get()
        return response.json()

    def create_batch_accounts(
        self,
        accounts: list[BatchAccountDict],
    ):
        self.Handler.url = f"{self.requestUrl}/batch"
        payload: dict[str, Any] = {
            "accounts": accounts,
        }
        response = self.Handler.post(
            data=payload,
        )
        print(response.json())
        return response.json()


payload = {
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
            "accountCurrency": "USD",
            "accountNumber": "123456789",
        },
    ]
}

if __name__ == "__main__":
    tva = TatumVirtualAccounts()
    # print(tva.generate_virtual_account(data=payload))
    # print(tva.list_all_virtual_accounts())
    # print(tva.get_account_entities_count())
    # print(tva.get_account_balance(account_id="0x1c0a4c3c7a3e2c6a1b3d6c4b7b3f9b7c9b1c0a4c3c7a3e2c6a1b3d6c4b7b3f9b7c9"))
    print(tva.create_batch_accounts(accounts=payload["accounts"]))
