from enum import Enum
from typing import Mapping, Any

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


class BnbSmartChain:

    def __init__(self) -> None:
        """
        Initializes the BNB SmartChain with the base URL for BCH wallet-related API requests
        and a RequestHandler for making the HTTP requests.
        """
        self.requestUrl = f"{creds.TATUM_BASE_URL}bsc/wallet"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def generate_wallet(self) -> Mapping[str, Any]:
        response = self.Handler.get()
        return response.json()

    def generate_address(self, xpub: str, *, index: int = 0) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bsc/address/{xpub}/{index}"
        response = self.Handler.get()
        return response.json()

    def generate_private_key(self, mnemonic: str, index: int = 0) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bsc/wallet/priv"
        payload = {"index": index, "mnemonic": mnemonic}
        response = self.Handler.post(data=payload)
        return response.json()

    def get_current_block(self) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bsc/block/current"
        response = self.Handler.get()
        return response.json()

    def get_block_hash(self, block_hash: int) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bsc/block/{block_hash}"
        response = self.Handler.get()
        return response.json()

    def get_balance(self, address: str) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bsc/account/balance/{address}"
        response = self.Handler.get()
        return response.json()

    def get_transactions(self, hash_value: str) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bsc/transaction/{hash_value}"
        response = self.Handler.get()
        return response.json()

    def get_outgoing_transactions(self, address: str) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bsc/transaction/count/{address}"
        response = self.Handler.get()
        return response.json()

    def send_bsc_bep20(
            self,
            *,
            to_address: str,
            amount: int | float,
            sender_private_key: str,
            currency: Currency = Currency.BSC.value,
            gas_price: int | float = None,
            gas_limit: int | float = None,
            nonce: int | None = None,
            data: str | None = None

    ) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bsc/transaction"
        payload = {
            "data": data,
            "nonce": nonce,
            "to": to_address,
            "currency": currency,  # enum value e.g Currency.BSC.value
            'amount': amount,
            "fee": None if gas_limit is None and gas_limit is None else {
                'gasPrice': gas_price,
                'gasLimit': gas_limit
            },
            'fromPrivateKey': sender_private_key
        }
        response = self.Handler.post(data=payload)
        return response.json()

    def invoke_smart_contract_method(self, contract_address: str, method_name: str, method_abi: Mapping[str, Any],
                                     params: list[str]) -> Mapping[str, Any]:
        self.Handler.url = f"{creds.TATUM_BASE_URL}bsc/smartcontract"
        payload = {
            "contractAddress": contract_address,
            "methodName": method_name,
            "methodABI": method_abi,
            "params": params
        }
        response = self.Handler.post(data=payload)
        return response.json()




if __name__ == "__main__":
    data = {
        "contract_address": "0x687422eEA2cB73B5d3e242bA5456b782919AFc85",
        "method_name": "transfer",
        "method_abi": {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256"
                }
            ],
            "name": "stake",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        "params": [
            "0x632"
        ]
    }
    wallet = BnbSmartChain()
    print(wallet.invoke_smart_contract_method(**data))
