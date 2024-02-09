# from tatum.tatum_client import creds
from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler

requestUrl = f"{creds.TATUM_BASE_URL}solana/wallet"

# create an instance of the RequestHandler class
Handler = RequestHandler(
    requestUrl,
    {
        "Content-Type": "application/json",
        "x-api-key": creds.TATUM_API_KEY,
    },
)


class SolanaWallet:

    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}solana/wallet"

        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def generate_solana_wallet():
        """
        Generates a new Solana wallet.
        """
        print(f"TATUM_API_KEY: {creds.TATUM_API_KEY}")
        # create a new wallet
        response = Handler.get()
        # return the wallet address and private key
        # #TODO: return ONLY the wallet address; encrypt the private key in Tatum Key Manager System
        return response.json()


if __name__ == "__main__":
    solana = SolanaWallet()
    sol_wallet = solana.generate_solana_wallet()
    print(sol_wallet)
