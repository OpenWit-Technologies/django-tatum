from tatum_client import creds
from utils.requestHandler import RequestHandler


class TatumVirtualAccounts:
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}ledger/account"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def generate_virtual_account(self, data: dict):
        response = self.Handler.post(data)
        return response.json()

    def list_all_virtual_accounts(self, query: dict = None):
        if query is None:
            query = {}
        response = self.Handler.get(params=query)
        return response.json()

    def get_account_balance(self, account_id: str):

        requestUrl = f"{creds.TATUM_BASE_URL}ledger/account/{account_id}/balance"
        Handler = RequestHandler(
            requestUrl, {"x-api-key": creds.TATUM_API_KEY}
        )

        response = Handler.get()
        return response.json()
