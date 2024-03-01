from enum import Enum
from typing import Mapping, Any
import datetime

from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class Currency(Enum):
    BSC = "BSC"
    BETH = "BETH"
    BBTC = "BBTC"
    RMD = "RMD"
    USDC_BSC = "USDC_BSC"
    B2U_BSC = "B2U_BSC"
    BADA = "BADA"
    WBNB = "WBNB"
    GMC_BSC = "GMC_BSC"
    BDOT = "BDOT"
    BXRP = "BXRP"
    BLTC = "BLTC"
    BBCH = "BBCH"
    HAG = "HAG"
    CAKE = "CAKE"
    BUSD_BSC = "BUSD_BSC"


class BnbBeaconChain:

    def __init__(self) -> None:
        """
        Initializes the BNB BeaconChain with the base URL for BCH wallet-related API requests
        and a RequestHandler for making the HTTP requests.
        """
        self.requestUrl = f"{creds.TATUM_BASE_URL}bnb"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def get_current_block(self) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bnb/block/current"
        response = self.Handler.get()
        return response.json()

    def get_transaction_by_block(self, block_height: int) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bnb/block/{block_height}"
        response = self.Handler.get()
        return response.json()

    def get_account_detail(self, address: str) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bnb/account/{address}"
        response = self.Handler.get()
        return response.json()

    def get_transaction_by_hash(self, block_hash: int) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bnb/transaction/{block_hash}"
        response = self.Handler.get()
        return response.json()

    def get_transaction_by_address(self, address: str, start_time: datetime, end_time: datetime, *args, **kwargs) -> \
            Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bnb/account/transaction/{address}"
        query = {
            "startTime": start_time,  # Start time in milliseconds e.g startTime=1651831727871
            "endTime": end_time
        }
        response = self.Handler.get(params=query)
        return response.json()

    def send_bnb_beacon(
            self,
            *,
            to_address: str,
            currency: Currency = Currency.BSC.value,
            amount: int | float,
            sender_private_key: str,
            message: str | None = None

    ) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bnb/transaction"
        payload = {
            "to": to_address,
            "currency": currency,  # enum value e.g Currency.BSC.value
            'amount': amount,
            'fromPrivateKey': sender_private_key,
            'message': message
        }
        response = self.Handler.post(data=payload)
        return response.json()

    def broadcast_transaction(self, tx_data: str, signature_id: str = None) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/broadcast"
        payload = {"txData": tx_data, "signatureId": signature_id}
        response = self.Handler.post(data=payload)
        return response.json()


if __name__ == "__main__":
    wallet = BnbBeaconChain()
    data = {
        "tx_data": "62BD544D1B9031EFC330A3E855CC3A0D51CA5131455C1AB3BCAC6D243F65460D"
    }
    print(wallet.broadcast_transaction(**data))
