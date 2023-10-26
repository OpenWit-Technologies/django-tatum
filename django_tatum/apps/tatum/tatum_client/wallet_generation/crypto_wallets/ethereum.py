from django_tatum.apps.tatum.tatum_client import creds 
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler

class EthereumWallet:
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}ethereum/wallet"
        
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )
        
    def generate_ethereum_wallet(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}ethereum/wallet"
        
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )
        
        response = self.Handler.get()
        return response.json()
    
if __name__ == "__main__":
    ethereum = EthereumWallet()
    eth_wallet = ethereum.generate_ethereum_wallet()
    print(eth_wallet)

