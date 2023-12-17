from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import BaseRequestHandler
from django_tatum.apps.tatum.utils.response_handlers import handle_response_object


class BlockchainFees(BaseRequestHandler):
    def __init__(self):
        """Initialize TatumVirtualCurrency class."""
        self.setup_request_handler("blockchain/")
        super().__init__()

    def get_recommended_gas_price(self, chain: str):
        """Get the recommended fee/gas price for a blockchain.

        Fee is in satoshis(meaning currency(BTC, DOGE,... / 100 000 000) per byte

        This API is supported for the following blockchains:

            Bitcoin
            Dogecoin
            Ethereum
            Litecoin

        Args:
            chain (str): Blockchain to get recommended gas price for.
            Acceptable Enum: "ETH" "BTC" "LTC" "DOGE"

        Returns:
            [type]: [description]
        """
        self.setup_request_handler(f"blockchain/fee/{chain}")
        response: str = handle_response_object(self.Handler.get())
        return response

    # def estimate_fee_for_transaction_on_a_blockchain(self, )
