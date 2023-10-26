from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class PolygonMatic():
    def __init__(self) -> None:
        self.requestUrl = f"{creds.TATUM_BASE_URL}polygon/wallet"
        
        # create an instance of the RequestHandler class
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )


    # TODO: Create a class with functions for generating all the crypto wallets
    def generate_polygon_wallet(self):
        """
        Generates a new Polygon wallet.
        """
        print(f"TATUM_API_KEY: {creds.TATUM_API_KEY}")
        # create a new wallet
        response = self.Handler.get()
        # return the wallet address and private key #TODO: return ONLY the wallet address; encrypt the private key in Tatum Key Manager System
        return response.json()
    
    def generate_private_key(self, payload: dict):
        priv_url = f"{self.requestUrl}/priv"
        
        validate = ['index', 'mnemonic']
        for val in validate:
            if val not in payload.keys():
                raise Exception(f"{val} is a required field")
        private_key_handler = RequestHandler(
            priv_url,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )
        response = private_key_handler.post(data=payload)
        return response.json()
    
if __name__ == "__main__":
    polygon = PolygonMatic()
    pol_wallet = polygon.generate_polygon_wallet()
    print(pol_wallet)


