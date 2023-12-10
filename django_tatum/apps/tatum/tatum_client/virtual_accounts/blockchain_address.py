from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class TatumBlockchainAdress:
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}offchain/account"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def create_deposit_address(self, account_id: str):
        self.requestUrl = f"{self.requestUrl}/{account_id}/address"
        self.Handler = RequestHandler(
            self.requestUrl,
            {"x-api-key": creds.TATUM_API_KEY},
        )

        response = self.Handler.post()
        return response.json()


if __name__ == "__main__":
    tatum_blockchain_address = TatumBlockchainAdress()
    account_id = "656cbfa574d8e8cd7f1db8ad"
    tba = tatum_blockchain_address.create_deposit_address(account_id)
    print(tba)
