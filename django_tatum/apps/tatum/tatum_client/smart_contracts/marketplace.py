from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class Marketplace:
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}blockchain/marketplace/listing"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def create_marketplace_contract_onchain(
        self,
        chain: str,
        feeRecipient: str,
        marketplaceFee: int,
        fromPrivateKey: str,
        nonce: int = None,
        fee: dict = None,
    ):
        pass
