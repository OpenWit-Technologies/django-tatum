from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class AlgorandWallet:
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}algorand/wallet"

        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def generate_wallet(self):
        response = self.Handler.get()
        return response.json()

    def generate_account_address(self, wallet_private_key: str):
        self.Handler.url = f"{creds.TATUM_BASE_URL}algorand/address/{wallet_private_key}"
        response = self.Handler.get()
        return response.json()

    def get_account_balance(self, wallet_address: str):
        self.Handler.url = f"{creds.TATUM_BASE_URL}algorand/account/balance/{wallet_address}"
        response = self.Handler.get()
        return response.json()

    def get_current_block_number(self):
        self.Handler.url = f"{creds.TATUM_BASE_URL}algorand/block/current"
        response = self.Handler.get()
        return response.json()

    def get_block_by_round_number(self, round_number: int):
        self.Handler.url = f"{creds.TATUM_BASE_URL}algorand/block/{round_number}"
        response = self.Handler.get()
        return response.json()

    def send_to_algo_account(
        self,
        *,
        sender_address: str,
        receiver_address: str,
        amount: str,
        sender_private_key: str,
        fee: str = None,
        note: str = None,
    ):
        self.Handler.url = f"{creds.TATUM_BASE_URL}algorand/transaction"

        payload = {
            "from": sender_address,
            "to": receiver_address,
            "fee": fee,
            "amount": amount,
            "note": note,
            "fromPrivateKey": sender_private_key,
        }
        response = self.Handler.post(data=payload)
        return response.json()

    def enable_receive_asset_on_account(self, asset_id: int, from_private_key: str, fee: str | None = None):
        self.Handler.url = f"{creds.TATUM_BASE_URL}algorand/asset/receive"

        payload = {"assetId": asset_id, "fromPrivateKey": from_private_key, "fee": fee}
        response = self.Handler.post(data=payload)
        return response.json()

    def get_transaction(self, txid: str):
        self.Handler.url = f"{creds.TATUM_BASE_URL}algorand/transaction/{txid}"
        response = self.Handler.get()
        return response.json()

    def broadcast_transaction(self, txData: str, signature_id: str | None = None, index: int | None = None):
        self.Handler.url = f"{creds.TATUM_BASE_URL}algorand/broadcast"

        payload = {"txData": txData, "signatureId": signature_id, "index": index}
        response = self.Handler.post(data=payload)
        return response.json()


if __name__ == "__main__":
    wallet = AlgorandWallet()
    print(wallet.broadcast_transaction("62BD544D1B9031EFC330A3E855CC3A0D51CA5131455C1AB3BCAC6D243F65460D"))
